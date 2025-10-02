## Running with Docker

1. **Create `.env` file**
   - Place the `.env` file in the root of the project (same level as `pyproject.toml`).
   - Use `.env.example` as a template.
   - If `.env` is not created, `.env.template` values will be used by default.

2. **Start containers**
```bash
docker compose up -d --build
```

3. **Create a superuser (optional)**
```bash
docker exec -it django python esn/manage.py createsuperuser
```

4. **Populate the database (optional)**
```bash
docker exec -it django python esn/manage.py fill_network_nodes --count 30
```
- The `--count` argument specifies the number of network objects. Default is 10.

5. **Access the application**
- Application URL: `http://localhost:DJANGO_PORT/` (replace `DJANGO_PORT` with the value from your `.env`).
- Swagger docs available at `http://localhost:DJANGO_PORT/docs/` if `DEBUG=True`.

---

## Running Locally

1. **Create `.env` file**
   - Place the `.env` file in the root of the project (same level as `pyproject.toml`).
   - Use `.env.example` as a template.
   - If `.env` is not created, `.env.template` values will be used by default.

2. **Update `settings.py`**
- Comment Docker blocks and uncomment Local blocks:
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

3. **Start required containers**
```bash
docker compose up -d pg rabbitmq
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Populate the database (optional)**
```bash
python manage.py fill_network_nodes --count 30
```
- `--count` specifies the number of network objects, default is 10.

7. **Run the application**
```bash
python manage.py runserver
```
- Application URL: `http://localhost:8000/`
- Swagger docs available at `http://localhost:8000/docs/` if `DEBUG=True`.
