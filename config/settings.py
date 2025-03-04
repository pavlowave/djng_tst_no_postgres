import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Определение базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Конфиденциальные ключи
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in environment variables")

DEBUG = os.getenv("DEBUG") == "True"

# Разрешенные хосты
ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "localhost", "pavlowave.pythonanywhere.com"]

# Определение установленных приложений
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "modules.products",  # Приложение товаров
]

# Определение middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Корневой URL конфигурации
ROOT_URLCONF = "config.urls"

# Настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = "config.wsgi.application"

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Локализация
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статические файлы
STATIC_URL = "/static/"

# Поле первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Настройки Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")

# Ключи Stripe для разных валют
STRIPE_KEYS = {
    "usd": {
        "secret": os.getenv("STRIPE_USD_SECRET"),
        "public": os.getenv("STRIPE_USD_PUBLIC"),
    },
    "eur": {
        "secret": os.getenv("STRIPE_EUR_SECRET"),
        "public": os.getenv("STRIPE_EUR_PUBLIC"),
    }
}
