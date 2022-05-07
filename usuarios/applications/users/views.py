import email
from re import template
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    View 
)
from django.views.generic.edit import (
    FormView
)
from .functions import code_generator 
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm
from .models import User

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    
    def form_valid(self, form):
        # Modelo User usa, un manager, que tiene contructores.
        #estos manager tiene a _create_user(), ahi pasamos los params para instanciar.
        #si tenemos params que no esta mencionados en los contructres, los recibimos como extra_ields
        # y los mandamos, como aca, por palabra clave.(nombres, apellidos y genero)
        codigo = code_generator()
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            #extra_fields: campos no nombranos ind en los metodos contructores.
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro=codigo
        )
        #envio de codigo de mail
        asunto = 'Confirmacion de email'
        mensaje = 'Codigo de Verificacion: ' + codigo
        email_remitente = 'fedefenker386@gmail.com'
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        #
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification'
            )
        )

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')
    
    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)
    
class LogoutView(View):
     
     def get(self, request, *args, **kwargs):
         logout(request)
         return HttpResponseRedirect(
             reverse('users_app:user-login')
         )
class UpdatePasswordView(LoginRequiredMixin ,FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')
    
    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
            )
        if user:
            new_pass = form.cleaned_data['password2']
            usuario.set_password(new_pass)
            usuario.save()
        return super(UpdatePasswordView, self).form_valid(form)

class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')
    def form_valid(self, form):
        return super(CodeVerificationView, self).form_valid(form)
        