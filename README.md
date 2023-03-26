# API Yamdb

## Описание проекта:
Это учебный проект по работе с API. Данная платформа собирает отзывы и комментарии пользователей на произведения.

## Технологии в проекте:
- Python 3.7.8
- Django 3.2.0
- Django REST Framework 3.12.4
- SQLite 3.41.1
- Simple JWT 5.2.2

## Инструкции по запуску:
1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:IvanErokhin/api_yamdb.git
```
2. Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
* Если у вас Linux/macOS:
    ```
    source venv/bin/activate
    ```
* Если у вас windows:

    ```
    source venv/scripts/activate
    ```
3. Обновить пакетный менеджер pip и установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip

pip install -r requirements.txt
```
4. Выполнить миграции:
```
cd api_yamdb/

python manage.py migrate
```
5. Импорт csv-файлов в базу данных:
    * Запускаем терминал Command Prompt и вводим команды:

        ```
        cd api_yamdb

        sqlite3.exe db.sqlite3
        ```
    * Далее вводим команды:

        ```
        .mode csv

        .import static/data/category.csv reviews_category
        ```
    * Повторяем последнюю команду для импорта каждого файла:

        ```
        .import static/data/comments.csv reviews_comment

        .import static/data/genre_title.csv reviews_genretitle

        .import static/data/genre.csv reviews_genre

        .import static/data/review.csv reviews_review

        .import static/data/titles.csv reviews_title

        .import static/data/users.csv user_user
        ```

6. Запустить проект:

```
python manage.py runserver
```

## Примеры запросов:
### 1. GET-запрос на получение списка всех произведений:
>`http://127.0.0.1:8000/api/v1/titles/`

Ответ:
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [...],
    "category": "string"
}
```
### 2. PATCH-запрос на обновление отзыва по id:
>`http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/`
```
{
    "text": "string",
    "score": 1
}
```
Ответ:
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```

### 3. POST-запрос на получение JWT-токена:
`http://127.0.0.1:8000/api/v1/auth/token/`
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
Ответ:
```
{
    "token": "string"
}
```

## Авторы:
[Ерохин Иван](https://github.com/IvanErokhin)

[Подойников Роман](https://github.com/RomanPodoynikov)

[Агашкина Алена](https://github.com/MAlena-ind)