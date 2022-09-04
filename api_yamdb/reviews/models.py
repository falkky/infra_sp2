from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import CreatedModel
from core.validators import validate_range

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
)


class User(AbstractUser):
    """
    Переопределяем модель User для добавления необходимых полей.
    """
    bio = models.TextField(blank=True, verbose_name='Информация')
    role = models.CharField(
        max_length=20,
        choices=CHOICES,
        default=USER,
        verbose_name='Роль пользователя'
    )
    confirmation_code = models.CharField(
        max_length=36,
        blank=True,
        null=True,
        verbose_name='Код подтверждения'
    )

    class Meta:
        verbose_name_plural = 'Пользователи'


class Categories(models.Model):
    """Модель для категорий произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        db_index=True,
        verbose_name='Slug категории',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Категории'


class Genres(models.Model):
    """Модель для жанров произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        db_index=True,
        verbose_name='Slug жанра',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель для названий произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выхода произведения',
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenresTitles',
        verbose_name='Жанр произведения',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-year',)
        verbose_name_plural = 'Произведения'


class GenresTitles(models.Model):
    """Модель для соответствия жанров и названий произведений"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='ID произведения',
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='ID жанра',
    )


class Review(CreatedModel):
    """Модель для обзоров на произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='ID произведения',
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[validate_range(1, 10)]
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__range=(1, 10)),
                name='score_range_1_10'
            ),
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='author_make_one_review_on_one_title'
            )
        ]


class Comments(CreatedModel):
    """Модель для комментариев на обзоры."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Текст комментария')

    text = models.TextField(verbose_name='Текст комментария',)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Комментарии'
