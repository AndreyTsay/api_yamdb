from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)
from django.db import models

from api_yamdb.settings import LENGTH_TEXT
from users.models import User
from api.validators import validate_me, validate_year


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Hазвание',
                            db_index=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=(validate_me, )
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Genre(models.Model):

    name = models.CharField(max_length=75,
                            verbose_name='Hазвание',
                            db_index=True)
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=(validate_me, )
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Title(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Hазвание',
        db_index=True
    )
    year = models.PositiveIntegerField(
        verbose_name='год выпуска',
        validators=(validate_year, ),
        db_index=True
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='жанр'

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        blank=False, verbose_name='Оцените от 1 до 10',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_review"
            )
        ]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
