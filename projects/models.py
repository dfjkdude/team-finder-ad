from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from . import constants

User = get_user_model()


class Project(models.Model):
    name = models.CharField(verbose_name='Название проекта',
                            max_length=constants.NAME_MAX_LENGTH)
    description = models.TextField(verbose_name='Описание проекта',
                                   blank=True)
    owner = models.ForeignKey(User,
                              verbose_name='Автор проекта',
                              related_name='owned_projects',
                              null=True,
                              on_delete=models.SET_NULL)
    created_at = models.DateTimeField(verbose_name='Дата создания проекта',
                                      auto_now_add=True)
    github_url = models.URLField(verbose_name='Ссылка на GitHub', blank=True,
                                 null=True)
    status = models.CharField(verbose_name='Статус проекта',
                              choices=[
                                  (constants.STATUS_OPEN, "Открыт"),
                                  (constants.STATUS_CLOSED, "Закрыт")
                              ],
                              max_length=constants.STATUS_MAX_LENGTH,
                              default=constants.STATUS_OPEN)
    participants = models.ManyToManyField(User,
                                          verbose_name='Участники проекта',
                                          blank=True,
                                          related_name='participated_projects')

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'Проекты'

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Проект {self.name} от пользователя {self.owner}'
