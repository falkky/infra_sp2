# Проект YaMDb

## Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).

## Шаблон наполнения env-файла
- Указываем, что работаем с postgresql:
```
DB_ENGINE=django.db.backends.postgresql
```
- Имя базы данных:
```
DB_NAME=postgres
```
- Логин для подключения к базе данных:
```
POSTGRES_USER=postgres
```
- Пароль для подключения к БД (установите свой):
```
POSTGRES_PASSWORD=postgres
```
- Название сервиса (контейнера):
```
DB_HOST=db
```
- Порт для подключения к БД:
```
DB_PORT=5432
```

## Для запуска приложения в контейнерах
- Запустить проект:
```
docker-compose up -d
```
- Выполнить миграции:
```
docker-compose exec web python manage.py migrate
```
- Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
- Собираем статику проекта:
```
docker-compose exec web python manage.py collectstatic --no-input
```

## Основные endpoints
```
"auth": "http://127.0.0.1:8000/api/v1/auth/"
```
```
"users": "http://127.0.0.1:8000/api/v1/users/"
```
```
"categories": "http://127.0.0.1:8000/api/v1/categories/"
```
```
"genres": "http://127.0.0.1:8000/api/v1/genres/"
```
```
"titles": "http://127.0.0.1:8000/api/v1/titles/"
```

## Автор
Andrew Stepanov

## Используемые технологии
- Django
- Django REST
- Simple JWT
- Docker
- Docker-compose
- Nginx
- Gunicorn
- PostgeSQL
