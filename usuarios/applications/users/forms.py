from django import forms
from .models import User
from django.contrib.auth import authenticate
class UserRegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        #para personalizar 
        widget=forms.PasswordInput(
            attrs= {
                'placeholder': 'Contraseña'
            }
    ))
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        #para personalizar 
        widget=forms.PasswordInput(
            attrs= {
                'placeholder': 'Repetir Contraseña'
            }
    ))
    class Meta:
        model = User
        fields = (
            'username',
            'nombres',
            'apellidos',
            'email',
            'genero',
        )
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')

class LoginForm(forms.Form):
    """LoginForm definition."""

    # TODO: Define form fields here
    username = forms.CharField(
        label='Usuario',
        required=True,
        #para personalizar 
        widget=forms.TextInput(
            attrs= {
                'placeholder': 'Usuario'
            }
    ))
    password = forms.CharField(
        label='Contraseña',
        required=True,
        #para personalizar 
        widget=forms.PasswordInput(
            attrs= {
                'placeholder': 'Contraseña'
            }
    ))
    #metodos para validar el pass
    def clean(self):
        #el diccionario del padre.
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        # si no es valido-> tira error
        if not authenticate(username= username, password = password):
            raise forms.ValidationError('Los datos no son correctos')
        #si es valido, devuelve el diccionario.
        return self.cleaned_data
class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        #para personalizar 
        widget=forms.PasswordInput(
            attrs= {
                'placeholder': 'Contraseña Actual'
            }
    ))
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        #para personalizar 
        widget=forms.PasswordInput(
            attrs= {
                'placeholder': 'Contraseña Nueva'
            }
    ))
class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)
    