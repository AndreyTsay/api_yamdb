from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class User(AbstractBaseUser):
    ROLES = (
        ('User', 'User'),
        ('Moderator', 'Moderator'),
        ('Admin', 'Admin'),
    )

    username = models.CharField(max_length=150, unique=True,
                                verbose_name='Никнейм пользователя')
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name="Почта")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    bio = models.TextField(verbose_name="Инфа о пользователе")

    role = models.CharField(max_length=9, choices=ROLES, default='User')
    USERNAME_FIELD = ['username', 'email']

    def __str__(self):
        return self.username


