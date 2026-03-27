from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as DjangoLoginView, PasswordResetView, PasswordResetConfirmView
from django.views.decorators.http import require_http_methods
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
import re


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Dirección de email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': '',
            'autocomplete': 'off',
            'readonly': 'readonly'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not User.objects.filter(email=email).exists():
            raise forms.ValidationError('No hay cuenta registrada con este email.')
        return email


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Contraseña',
        min_length=8,
        help_text='Mínimo 8 caracteres. Incluye mayúsculas, minúsculas y números.'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmar contraseña'
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        labels = {
            'email': 'Dirección de email',
            'username': 'Nombre de usuario',
        }
        error_messages = {
            'email': {
                'required': 'El email es obligatorio.',
            },
            'username': {
                'required': 'El nombre de usuario es obligatorio.',
                'unique': 'Este nombre de usuario ya está en uso.',
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Validar formato básico de email
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                raise forms.ValidationError('Ingresa un email válido.')
            # Validar que el email no exista
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Este email ya está registrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Validar caracteres permitidos
            if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
                raise forms.ValidationError('Solo se permiten letras, números, guiones y puntos.')
            # Validar longitud mínima
            if len(username) < 3:
                raise forms.ValidationError('El nombre de usuario debe tener al menos 3 caracteres.')
            # Validar que no exista
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            # Validar longitud
            if len(password) < 8:
                raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
            # Validar que incluya mayúsculas
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError('La contraseña debe incluir al menos una mayúscula.')
            # Validar que incluya minúsculas
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError('La contraseña debe incluir al menos una minúscula.')
            # Validar que incluya números
            if not re.search(r'[0-9]', password):
                raise forms.ValidationError('La contraseña debe incluir al menos un número.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'

