from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'название',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'описание',
        max_length=256,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


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
