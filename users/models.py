from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from . import constants
from .managers import UserManager
from .utils import generate_avatar


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,
                              verbose_name='Адрес электронной почты')
    name = models.CharField(max_length=constants.NAME_MAX_LENGTH,
                            verbose_name='Имя')
    surname = models.CharField(max_length=124,
                               verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='avatars/',
                               verbose_name='Аватарка пользователя',
                               blank=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона',
                             unique=True, null=True, blank=True)
    github_url = models.URLField(blank=True, verbose_name='Ссылка на GitHub',
                                 null=True)
    about = models.TextField(max_length=256, blank=True,
                             verbose_name='Обо мне')
    is_active = models.BooleanField(verbose_name='Активный пользователь',
                                    default=True)
    is_staff = models.BooleanField(verbose_name='Администратор', default=False)
    favorites = models.ManyToManyField('projects.Project',
                                       verbose_name='Избранные проекты',
                                       blank=True,
                                       related_name='interested_users')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.pk:
            name = self.name
            avatar_file = generate_avatar(name)
            self.avatar.save(avatar_file.name, avatar_file, save=False)
        try:
            identify_hasher(self.password)
        except ValueError:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'
