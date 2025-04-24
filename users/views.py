import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.core.mail import send_mail

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserPasswordResetForm
from users.models import User


# Create your views here.

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False

        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/confirm_register/{token}'

        send_mail(
            subject='Подтверждение регистрации',
            message=f'Здравствуйте, перейдите по ссылке для подтверждения почты {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)


class RegisterConfirmView(TemplateView):
    template_name = 'users/confirm_register.html'
    def post(self, request, *args, **kwargs):
        token = kwargs.get('token')
        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.save()
        return redirect(reverse('users:login'))


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')


    def form_valid(self, form):
        email = form.cleaned_data['email']
        print(email)
        user = User.objects.get(email=email)
        uid = str(user.pk)
        token = user.token

        url = self.request.build_absolute_uri(reverse(
            'users:password_reset_confirm',
            kwargs={'uidb64': uid, 'token': token})
        )
        print(url)

        send_mail(
            subject='Сброс пароля',
            message=f'Чтобы завершить сброс пароля, перейдите по ссылке: {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        print('ok')

        return super().form_valid(form)


class UserPasswordResetDoneView(PasswordResetDoneView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/password_reset_complete.html'
    success_url = reverse_lazy('users:login')
