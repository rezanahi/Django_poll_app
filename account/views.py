from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponseBadRequest
from .tokens import account_activation_token


class LoginUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request, template_name='account/Login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, template_name='account/Login.html', context={'form': form})
        else:
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return render(request, template_name='account/Login.html', context={'form': form})
            login(request, user)
            return redirect('polls:index')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')


class RegisterUser(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, template_name='account/Register.html', context={'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, template_name='account/Login.html', context={'form': form})
        else:
            data = form.cleaned_data
            hashed_password = make_password(data['password'])
            user = User.objects.create(
                username=data['username'],
                password=hashed_password,
                email=data['email'],
                is_active=False
            )
            user.save()

            # Send email confirmation
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account:account_activation_sent')


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:account_activation_complete')
        else:
            return HttpResponseBadRequest('Activation link is invalid!')


class AccountActivationSent(View):
    def get(self, request):
        return render(request, 'account/account_activation_sent.html')


class AccountActivationComplete(View):
    def get(self, request):
        return render(request, 'account/account_activation_complete.html')