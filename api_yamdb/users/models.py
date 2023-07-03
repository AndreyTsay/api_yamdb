from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.
class User(AbstractUser):
    ROLES = (
        ('User', 'Обычный пользователь '),
        ('Moderator', 'Модератор'),
        ('Admin', 'Админ'),
    )

    username = models.CharField(max_length=150, unique=True,
                                verbose_name='Никнейм пользователя')
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name="Почта")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    bio = models.TextField(verbose_name="Инфа о пользователе")

    role = models.CharField(max_length=9, choices=ROLES, default='User',
                            verbose_name="Роль пользователя")
    confirmation_code = models.CharField(max_length=4, default='0000',
                                         verbose_name="Код подтверждения")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    @property
    def is_user(self):
        return self.role == User.ROLES[0][0]

    @property
    def is_moderator(self):
        return self.role == User.ROLES[1][0]

    @property
    def is_admin(self):
        return self.role == User.ROLES[2][0]

    def __str__(self):
        return self.username
