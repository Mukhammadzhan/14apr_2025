import logging
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import logout

from clients.validators import validate_email_domain, validate_username, validate_password
from django.core.exceptions import ValidationError
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from clients.models import Client
from clients.utils import send_email

logger = logging.getLogger()


    
class RegistrationView(View):
    """Registration controller. There will be only get"""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name="reg.html")
    
    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        email = request.POST.get("email")
        raw_password = request.POST.get("password")

        try:
            validate_username(username)
            validate_email_domain(email)
            validate_password(raw_password)
        except ValidationError as ve:
            messages.error(request, str(ve))
            return render(request=request, template_name="reg.html")

        try:
            code = os.urandom(32).hex()
            Client.objects.create(
                email=email,
                username=username,
                password=make_password(raw_password),
                activation_code = code
            )
            send_email(
                template="account_activation.html",
                context={"username": username, "code": f"http://127.0.0.1:8000/activation/{username}/{code}"},
                to=email, title="Confirm your account",
            )
            messages.info(request=request, message="Succes Registration")
            return render(request=request, template_name="reg.html")
        except IntegrityError as ie:
            logger.error(msg="Ошибка уникальности поля", exc_info=ie)
            messages.error(request=request, message="Wrong login or email")
            return render(request=request, template_name="reg.html")
        except Exception as e:
            logger.error(msg="Something happend", exc_info=e)
            messages.error(request=request, message=str(e))
            return render(request=request, template_name="reg.html")


class LoginView(View):
    """Login Controller"""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name="login.html")
    
    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")
        client: Client | None = authenticate(
            request=request, username=username, password=password
        )
        if not client:
            messages.error(
                request=request,
                message="Wrong username or password"
            )
            return render(request=request, template_name="login.html")
        login(request=request, user=client)
        return redirect(to="base")
    
class ProfileView(LoginRequiredMixin, TemplateView):
    """Личный кабинет пользователя"""
    template_name = "profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""
    model = Client
    template_name = "profile_edit.html"
    fields = ['first_name', 'last_name', 'email', 'birthday', 'gender']
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление профиля"""
    model = Client
    template_name = "profile_delete.html"
    success_url = reverse_lazy('base')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        messages.success(request, "Ваш аккаунт был успешно удален")
        return response

class ActivationView(View):
    def get(self, request: HttpRequest, username: str, code: str) -> HttpResponse:
        client = Client.objects.filter(
            username=username,
            activation_code = code
        ).first()
        if not client:
            return HttpResponse(content="<h1>Ты кто?</h1>")
        client.is_active = True
        client.save(update_fields=["is_active"])
        return redirect(to="clients:login")

class ResetPasswordView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(template_name="reset_account.html", request=request)
        
    
    def post(self, request: HttpRequest) -> HttpResponse:
        username=request.POST.get('username')
        email=request.POST.get('email')
        client = Client.objects.filter(username=username, email=email).first()
        new_password = os.urandom(32).hex()
        if not client:
            return HttpResponse("<h1>Пользователь не найден</h1>")

        client.password = make_password(new_password)
        client.save(update_fields=["password"])
        send_email(
                template="reset_password.html",
                context={"username": username, "new_password": f"{new_password}"},
                to=email, title="Confirm your account",
            )
        return redirect(to="clients:login")