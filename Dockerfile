FROM python:3.11-slim-bullseye
WORKDIR /app
EXPOSE 8000

ENV DEV_PACKAGES="build-essential unixodbc-dev git libffi-dev curl gnupg2"\
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.5.1

# Устанавливаем пакеты, необходимые для сборки
RUN apt-get update && apt-get install --yes --no-install-recommends $DEV_PACKAGES

# Устанавливаем зависимости проекта
COPY pyproject.toml poetry.lock ./
RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-root

# Очищаем образ от лишних пакетов
RUN apt-get remove --yes --purge $DEV_PACKAGES
RUN rm -rf /var/lib/apt/lists/*

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

