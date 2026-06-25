import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ValidationError

from utils.mixins import GitHubURLValidationMixin

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(),
        strip=False
    )

    class Meta:
        model = User
        fields = ('name', 'surname', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Почта",
        widget=forms.EmailInput()
    )

    # Переопределяем поле пароля
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput()
    )


class UserUpdateForm(GitHubURLValidationMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^(\+7|8)(\d{10})$'
        if phone is None:
            return phone
        elif re.match(pattern, phone):
            if phone[0] == '8':
                phone = '+7' + phone[1:]
            return phone
        raise ValidationError("Недопустимый формат записи телефона")
