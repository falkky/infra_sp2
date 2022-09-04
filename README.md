# Проект YaMDb

## Описание:
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).

## Шаблон наполнения env-файла:
DB_ENGINE=django.db.backends.postgresql
# указываем, что работаем с postgresql
DB_NAME=postgres
# имя базы данных
POSTGRES_USER=postgres
# логин для подключения к базе данных
POSTGRES_PASSWORD=postgres
# пароль для подключения к БД (установите свой)
DB_HOST=db
# название сервиса (контейнера)
DB_PORT=5432
# порт для подключения к БД

## Для запуска приложения в контейнерах:
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
## Основные endpoints:
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
