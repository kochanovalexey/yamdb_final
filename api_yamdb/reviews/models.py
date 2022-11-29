from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


TITLE_SYMBOLS_RESTRICTION = 15


class User(AbstractUser):
    """Кастомная модель User, с дополнительными полями биографии и роли."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимые символы в имени пользователя'
        )],
        verbose_name='Ник пользователя',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электроннной почты'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия пользователя'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        max_length=254,
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )

    def __str__(self) -> str:
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Category(models.Model):
    """Класс Category описывает модель категорий произведений."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс Genre описывает модель жанров произведений."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс Title описывает модель произведений, публикуемых на сайте."""

    name = models.CharField(max_length=300)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre,
                                   related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name[:TITLE_SYMBOLS_RESTRICTION]


class Review(models.Model):
    """Класс Review описывает модель отзывов, публикуемых на сайте."""

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveIntegerField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews', null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique_author_title')
        ]


class Comment(models.Model):
    """Класс Comment описывает модель комментариев, публикуемых на сайте."""

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments', null=True
    )
