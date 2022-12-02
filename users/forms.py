from .models import Users
from django.forms import ModelForm, TextInput, Textarea, PasswordInput, DateInput, DateTimeInput, EmailInput, \
    ImageField, forms


class LoginForm(ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'password']

        widgets = {
            'login': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'name': 'login'
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'name': 'password'
            })
        }


class RegistrationForm(ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'password']

        widgets = {
            'login': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин',
                'name': 'login'
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'name': 'password'
            }),
        }


class ResumeForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'last_name', 'birth_date', 'about', 'github_link', 'phone_number', 'specialization', 'email', 'telegram', 'login', 'profile_pic']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'name': 'name',
                'required': 'required'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия',
                'name': 'last_name'
            }),
            'birth_date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'День рождения',
                'name': 'birth_date',
                'type': 'date'
            }),
            'about': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Информация о вас',
                'name': 'about'
            }),
            'github_link': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ссылка на Github',
                'name': 'github_link'
            }),
            'phone_number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона',
                'name': 'phone_number'
            }),
            'telegram': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телеграм',
                'name': 'telegram'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта',
                'name': 'email',
                'type': 'email'
            }),
            'specialization': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Специализация',
                'name': 'specialization'
            }),
            'login': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин',
                'name': 'login'
            }),
        }
