from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField



class SignupForm(forms.ModelForm):
    """user signup form"""
    name = forms.CharField(label = "Nombre")
    last_name = forms.CharField(label = "Apellido",required = True)
    password = forms.CharField(label = "Contraseña",widget=forms.PasswordInput(),max_length = 64,required = True)
    email = forms.EmailField(required = True)
    phone = PhoneNumberField(region='MX', help_text="Con formato 521234567890")
    

    class Meta:
        model = get_user_model()
        fields = ('email','name','last_name', 'password','phone')


class LoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())