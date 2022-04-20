from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    View 
)
from django.views.generic.edit import (
    FormView
)
from .forms import UserRegisterForm, LoginForm
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
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            #extra_fields: campos no nombranos ind en los metodos contructores.
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
        )
        return super(UserRegisterView, self).form_valid(form)

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