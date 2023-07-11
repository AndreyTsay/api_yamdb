from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Админ'),)
LENGTH = 150


class User(AbstractUser):
    username = models.CharField(max_length=LENGTH, unique=True,
                                verbose_name='Никнейм пользователя')
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name="Почта")
    first_name = models.CharField(blank=True, max_length=LENGTH,
                                  verbose_name="Имя")
    last_name = models.CharField(blank=True, max_length=LENGTH,
                                 verbose_name="Фамилия")
    bio = models.TextField(blank=True, verbose_name="Инфа о пользователе")

    role = models.CharField(max_length=9, choices=ROLES, default=USER,
                            verbose_name="Роль пользователя")
    confirmation_code = models.CharField(max_length=10, default='0000000000',
                                         verbose_name="Код подтверждения")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff
