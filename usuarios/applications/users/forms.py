from django import forms
from .models import User

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