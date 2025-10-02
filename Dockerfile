FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . /app

CMD ["python", "esn/manage.py", "runserver", "0.0.0.0:8000"]
