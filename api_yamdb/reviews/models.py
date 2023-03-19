from django.db.models import (SET_NULL, CharField, ForeignKey, ManyToManyField,
                              Model, PositiveSmallIntegerField, SlugField,
                              TextField, CASCADE, IntegerField, DateTimeField,
                              UniqueConstraint)
from django.core.validators import MaxValueValidator, MinValueValidator


# Сделать импорт
# from ==== import User

# Create your models here.


# разместить под классом Title
class Review(Model):
    """Класс Reviews используется для создания отзывов.
    Экземпляр данного класса есть запись в таблице Review базы данных.
    """
    # title = ForeignKey(
    #     Title,
    #     on_delete=CASCADE,
    #     verbose_name='Произведение',
    #     related_name='reviews'
    # )
    title = IntegerField(default=1)   # temp.
    text = TextField('Текст отзыва')
    # author = ForeignKey(
    #     User,
    #     on_delete=CASCADE,
    #     verbose_name='Автор',
    #     related_name='reviews'
    # )
    author = IntegerField(default=1)   # temp.
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
    # review = ForeignKey(
    #     Review,
    #     on_delete=CASCADE,
    #     verbose_name='Отзыв',
    #     related_name='comments'
    # )
    review = IntegerField(default=1)   # temp.
    text = TextField()
    # author = ForeignKey(
    #     User,
    #     on_delete=CASCADE,
    #     verbose_name='Автор',
    #     related_name='comments'
    # )
    author = IntegerField(default=1)   # temp.
    pub_date = DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        """Метод строкового представления объекта."""
        return self.text

    class Meta:
        verbose_name = ('Комментарий к отзыву')
        verbose_name_plural = ('Комментарии к отзывам')
