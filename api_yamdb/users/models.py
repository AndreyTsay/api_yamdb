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

    role = models.CharField(max_length=9, choices=ROLES, default='User',
                            verbose_name="Роль пользователя")
    USERNAME_FIELD = ['username', 'email']
    REQUIRED_FIELDS = ('username', 'email',)

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


