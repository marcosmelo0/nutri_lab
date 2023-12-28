import os
from hashlib import sha256
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from .utils import password_is_valid, required_fields, send_email_html
from .models import Activation


def register(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('usuario')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not required_fields(username, email, password, confirm_password):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')

        if not password_is_valid(request, password, confirm_password):
            return redirect('/auth/register')

        try:
            user = User.objects.create_user(username=username, email=email,
                                            password=password, is_active=False)
            user.save()
            token = sha256(f"{username}{email}".encode()).hexdigest()
            activation = Activation(token=token, user=user)
            activation.save()

            path_template = os.path.join(settings.BASE_DIR, 'authentication/templates/emails/confirm_register.html')
            send_email_html(path_template, 'Cadastro Confirmado!', [email,], username=username, link_ativacao=f"127.0.0.1:8000/auth/active_account/{token}")
            messages.add_message(request, constants.SUCCESS, 'Registrado com sucesso!')

            return redirect('/auth/login')
        except:
            return redirect('/auth/register')


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect('/auth/login')
        else:
            auth.login(request, usuario)
            return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/auth/login')


def active_account(request, token):
    token = get_object_or_404(Activation, token=token)
    if token.active:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/login')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.active = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/login')
