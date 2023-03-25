from django.db.models import (SET_NULL, CharField, ForeignKey, ManyToManyField,
                              Model, PositiveSmallIntegerField, SlugField,
                              TextField, CASCADE, IntegerField, DateTimeField,
                              UniqueConstraint)

from django.core.validators import MaxValueValidator, MinValueValidator

# 2 это
# from django.contrib.auth import get_user_model
# User = get_user_model()
# на это
from user.models import User
# 2


# Create your models here.


class Category(Model):
    """Модель с категориями произведений."""
    name = CharField('Название категории', max_length=256)
    slug = SlugField('Slug категории', unique=True, max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(Model):
    """Модель с жанрами произведений."""
    name = CharField('Название жанра', max_length=256)
    slug = SlugField('Slug жанра', unique=True, max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(Model):
    """Модель с произведениями."""
    name = CharField('Название', max_length=256)
    year = PositiveSmallIntegerField('Год выпуска')
    description = TextField('Описание', blank=True, null=True)
    genre = ManyToManyField(Genre, through='GenreTitle')
    category = ForeignKey(
        Category,
        on_delete=SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(Model):
    """Модель, связующая жанры с произведениями."""
    genre = ForeignKey(Genre, on_delete=SET_NULL, null=True)
    title = ForeignKey(Title, on_delete=SET_NULL, null=True)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(Model):
    """Класс Reviews используется для создания отзывов.
    Экземпляр данного класса есть запись в таблице Review базы данных.
    """
    title = ForeignKey(
        Title,
        on_delete=CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    text = TextField('Текст отзыва')
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Автор',
        related_name='reviews'
    )
    # author = IntegerField(default=1)   # temp.
    score = IntegerField('Оценка', validators=[MinValueValidator(1),
                                               MaxValueValidator(10)])
    pub_date = DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        """Метод строкового представления объекта."""
        return self.text

    class Meta:
        verbose_name = ('Отзыв')
        verbose_name_plural = ('Отзывы')
        constraints = (
            UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'),
        )


class Comment(Model):
    """Класс Comment используется для создания комментариев к отзывам.
    Экземпляр данного класса есть запись в таблице Comment базы данных.
    """
    review = ForeignKey(
        Review,
        on_delete=CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    text = TextField()
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )
    # author = IntegerField(default=1)   # temp.
    pub_date = DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        """Метод строкового представления объекта."""
        return self.text

    class Meta:
        verbose_name = ('Комментарий к отзыву')
        verbose_name_plural = ('Комментарии к отзывам')
