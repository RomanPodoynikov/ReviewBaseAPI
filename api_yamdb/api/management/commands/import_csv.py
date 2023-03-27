import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.models import User


class Command(BaseCommand):
    """Команда для импорта csv-файлов в базу данных."""
    def import_user(self):
        """Функция для импорта в таблицу user."""
        with open(
            'api_yamdb/static/data/users.csv',
            encoding='utf8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != 'id':
                    User.objects.get_or_create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6],
                    )

    def import_category(self):
        """Функция для импорта в таблицу category."""
        with open(
            'api_yamdb/static/data/category.csv',
            encoding='utf8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != 'id':
                    Category.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    )

    def import_genre(self):
        """Функция для импорта в таблицу genre."""
        with open(
            'api_yamdb/static/data/genre.csv',
            encoding='utf8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != 'id':
                    Genre.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    )

    def import_titles(self):
        """Функция для импорта в таблицу title."""
        with open(
            'api_yamdb/static/data/titles.csv',
            encoding='utf8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != 'id':
                    category = Category.objects.get(id=row[3])
                    Title.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=category,
                    )

    def import_genre_title(self):
        """Функция для импорта в таблицу genretitle."""
        with open(
            'api_yamdb/static/data/genre_title.csv',
            encoding='utf8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != 'id':
                    title_id = Title.objects.get(id=row[1])
                    genre_id = Genre.objects.get(id=row[2])
                    GenreTitle.objects.get_or_create(
                        id=row[0],
                        title=title_id,
                        genre=genre_id,
                    )

    def import_review(self):
        """Функция для импорта в таблицу review."""
        with open(
            'api_yamdb/static/data/review.csv',
            encoding='utf8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != 'id':
                    title_id = Title.objects.get(id=row[1])
                    author = User.objects.get(id=row[3])
                    Review.objects.get_or_create(
                        id=row[0],
                        title=title_id,
                        text=row[2],
                        author=author,
                        score=row[4],
                        pub_date=row[5],
                    )

    def import_comments(self):
        """Функция для импорта в таблицу comment."""
        with open(
            'api_yamdb/static/data/comments.csv',
            encoding='utf8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != 'id':
                    review_id = Review.objects.get(id=row[1])
                    author = User.objects.get(id=row[3])
                    Comment.objects.get_or_create(
                        id=row[0],
                        review=review_id,
                        text=row[2],
                        author=author,
                        pub_date=row[4],
                    )

    def handle(self, *args, **options):
        self.import_user()
        self.import_category()
        self.import_genre()
        self.import_titles()
        self.import_genre_title()
        self.import_review()
        self.import_comments()
