from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import GeekUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    print(f"vk-oauth2: {response.keys()}")
    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'user_photo')),
                                                access_token=response['access_token'],
                                                v='5.95')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.geekuserprofile.gender = GeekUserProfile.MALE if data['sex'] == 2 else GeekUserProfile.FEMALE

    if data['about']:
        user.geekuserprofile.aboutMe = data['about']
    
    # if data['user_photo']:
    #     print(data['user_photo'])
    #     user.avatar = data['user_photo']

    if data['bdate']:
        print(data['bdate'])
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()
