# Используем базовый образ с Python
FROM python:3.11-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    wkhtmltopdf \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /app/

# Устанавливаем PYTHONPATH, чтобы Python знал, где искать модули
ENV PYTHONPATH=/app/cash_register

# Запуск миграций, опциональное заполнение базы данных и запуск сервера Django
CMD ["sh", "-c", "export DJANGO_SETTINGS_MODULE=cash_register.cash_register.settings && python manage.py migrate && python shop/populate_items.py && xvfb-run --auto-servernum -- python manage.py runserver 0.0.0.0:8000"]