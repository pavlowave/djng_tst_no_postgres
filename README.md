
<h1 align="center">Django + Docker + PostgreSQL Template</h1>

<div align="center">

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%23092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-%230db7ed?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
</div>

## Установка и запуск:

1. Клонирование репозитория:

```
git clone https://github.com/pavlowave/Docker-Django-Postgres
cd Docker-Django-Postgres
```

2. Создание .env файла:
Создайте файл .env в корне проекта с таким содержанием:

```bash
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_HOST=db
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
```

3. Сборка и запуск контейнеров
```bash
docker-compose up --build
```

4. Миграции базы данных После запуска контейнера выполните миграции для настройки базы данных:
```
docker-compose exec web-app python manage.py migrate
```
5. Доступ к приложению Приложение будет доступно по адресу: http://localhost:8000

## Структура проекта

* **Dockerfile**: Конфигурация для сборки образа Docker.
* **docker-compose.yml**: Описание сервисов (Django и PostgreSQL).
* **requirements.txt**: Список Python-зависимостей.
* **.env**: Конфиденциальные настройки (игнорируется в Git).
* **settings.py**: Подключение переменных окружения для конфигурации Django.

## Как использовать

Этот шаблон подходит для:

* Создания новых Django проектов.
* Изучения работы с Docker для Django приложений.
* Быстрого прототипирования веб-приложений.

## Заметки

* Убедитесь, что Docker и Docker Compose установлены на вашей машине.
* Этот шаблон использует минимальные настройки для разработки. Для продакшена рекомендуется обновить параметры безопасности и использовать менеджер секретов (например, AWS Secret
