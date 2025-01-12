# Используем базовый образ Python 3.9 на Alpine 3.16
FROM python:3.9-alpine3.16

# Устанавливаем переменные окружения
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем файл с зависимостями (requirements.txt) в контейнер
COPY requirements.txt /temp/requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Открываем порт 8000 для подключения (для Django)
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

# Устанавливаем Python-зависимости
RUN pip install -r /temp/requirements.txt

# Создаем нового пользователя service-user без пароля
RUN adduser --disabled-password service-user

# Переключаемся на пользователя service-user для выполнения команд в контейнере
USER service-user
