from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from django.db import transaction
from authapp.forms import GeekUserLoginForm, GeekUserRegisterForm, GeekUserEditForm, GeekUserProfileEditForm
from authapp.models import GeekUser


def send_verify_mail(user):
    verify_link = reverse('auth:verify', kwargs={
        'email': user.email,
        'activation_key': user.activation_key,
    })
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def login(request):
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST':
        form = GeekUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        form = GeekUserLoginForm()

    context = {
        'title': 'вход в систему',
        'form': form,
        'next': next
    }
    return render(request, 'authapp/login.html', context)


def verification_msg(request):
    context = {
        'title': 'Вурификация почты',
    }
    return render(request, 'authapp/verification_msg.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == 'POST':
        form = GeekUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:verification_msg'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = GeekUserRegisterForm()

    context = {
        'title': 'регистрация',
        'form': form
    }

    return render(request, 'authapp/register.html', context)

@transaction.atomic
def update(request):
    if request.method == 'POST':
        form = GeekUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = GeekUserProfileEditForm(request.POST, request.FILES,
                                               instance=request.user.geekuserprofile)
        
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:update'))
    else:
        form = GeekUserEditForm(instance=request.user)
        profile_form = GeekUserProfileEditForm(instance=request.user.geekuserprofile)

    context = {
        'title': 'редактирование',
        'form': form,
        'profile_form': profile_form,
    }

    return render(request, 'authapp/update.html', context)


def verify(request, email, activation_key):
    try:
        user = GeekUser.objects.get(email=email)
        if user.activation_key == activation_key and user.is_activation_key_valid():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            print(f'error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))