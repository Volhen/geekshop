from django import template
from django.conf import settings

register = template.Library()

def media_folder_cards(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    produccards_images_images/product1.jpg --> /media/cards_images/product1.jpg
    """
    if not string:
        string = 'cards_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    """
    if not string:
        string = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{string}'

register.filter('media_folder_cards', media_folder_cards)