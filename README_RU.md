**Изменить язык:** [English](README.md) | [Русский](README_RU.md)

## Запуск с помощью Docker

1. **Создайте файл `.env`**
   - Разместите файл `.env` в корне проекта (на одном уровне с `pyproject.toml`).
   - Используйте `.env.example` как шаблон.
   - Если `.env` не будет создан, будут использоваться значения из `.env.template`.

2. **Поднимите контейнеры**
```bash
docker compose up -d --build
```

3. **Создайте суперпользователя (опционально)**
```bash
docker exec -it django python esn/manage.py createsuperuser
```

4. **Заполните базу данных (опционально)**
```bash
docker exec -it django python esn/manage.py fill_network_nodes --count 30
```
- Аргумент `--count` указывает количество объектов сети. По умолчанию 10.

5. **Доступ к приложению**
- URL приложения: `http://localhost:DJANGO_PORT/` (замените `DJANGO_PORT` на значение из вашего `.env`).
- Swagger документация доступна по адресу `http://localhost:DJANGO_PORT/docs/`, если `DEBUG=True`.

---

## Локальный запуск

1. **Создайте файл `.env`**
   - Разместите файл `.env` в корне проекта (на одном уровне с `pyproject.toml`).
   - Используйте `.env.example` как шаблон.
   - Если `.env` не будет создан, будут использоваться значения из `.env.template`.

2. **Обновите `settings.py`**
- Закомментируйте блоки Docker и раскомментируйте Local блоки:
```python
# Local
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env("POSTGRES_DB"),
#         "USER": env("POSTGRES_USER"),
#         "PASSWORD": env("POSTGRES_PASSWORD"),
#         "HOST": env("POSTGRES_HOST"),
#         "PORT": env("POSTGRES_PORT"),
#     }
# }
```
```python
# Docker
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "pg",
        "PORT": 5432,
    }
}
```
```python
# Local
# CELERY_BROKER_URL = f"amqp://{env('RABBITMQ_USER')}:{env('RABBITMQ_PASSWORD')}@{env('RABBITMQ_HOST')}:{env('RABBITMQ_PORT')}//"

# Docker
CELERY_BROKER_URL = (
    f"amqp://{env('RABBITMQ_USER')}:{env('RABBITMQ_PASSWORD')}@rabbitmq:5672//"
)
```

3. **Поднимите необходимые контейнеры**
```bash
docker compose up -d pg rabbitmq
```

4. **Примените миграции**
```bash
python manage.py migrate
```

5. **Создайте суперпользователя (опционально)**
```bash
python manage.py createsuperuser
```

6. **Заполните базу данных (опционально)**
```bash
python manage.py fill_network_nodes --count 30
```
- `--count` указывает количество объектов сети, по умолчанию 10.

7. **Запустите приложение**
```bash
python manage.py runserver
```
- URL приложения: `http://localhost:8000/`
- Swagger документация доступна по адресу `http://localhost:8000/docs/`, если `DEBUG=True`.
