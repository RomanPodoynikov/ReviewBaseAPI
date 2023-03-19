from django.db.models import (DO_NOTHING, CharField, ForeignKey,
                              ManyToManyField, Model,
                              PositiveSmallIntegerField, SlugField, TextField)


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
        on_delete=DO_NOTHING,
        verbose_name='Категория',
        related_name='titles',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(Model):
    """Модель, связующая жанры с произведениями."""
    genre = ForeignKey(Genre, on_delete=DO_NOTHING)
    title = ForeignKey(Title, on_delete=DO_NOTHING)

    def __str__(self):
        return f'{self.genre} {self.title}'
