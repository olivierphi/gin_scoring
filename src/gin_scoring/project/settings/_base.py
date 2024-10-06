"""
Django settings for our project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from os import environ as env
from pathlib import Path

import dj_database_url

# points to our git repo's root
BASE_DIR = Path(
    env.get("DJANGO_BASE_DIR", str(Path(__file__).parent / ".." / ".." / ".." / ".."))
).resolve()

SECRET_KEY = env["SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS: list[str] = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps:
    "django_tailwind_cli",
    # Our own apps:
    "gin_scoring.apps.scoreboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gin_scoring.project.urls"

TEMPLATES = [
    {
        # @link https://docs.djangoproject.com/en/5.1/topics/templates/#django.template.backends.jinja2.Jinja2
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "gin_scoring.project.jinja2.environment",
        },
    },
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

WSGI_APPLICATION = "gin_scoring.project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
    )
}

# Sessions
# https://docs.djangoproject.com/en/5.1/topics/http/sessions/

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

# File storage
# https://docs.djangoproject.com/en/5.1/ref/settings/#storages
STORAGES = {
    # This is a copy of the Django default value for this setting.
    # We'll alter it in some of our settings modules.
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

_scoreboard_app_path = BASE_DIR / "src" / "gin_scoring" / "apps" / "scoreboard"
STATICFILES_DIRS = [
    _scoreboard_app_path / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Tailwind CSS
# https://django-tailwind-cli.andrich.me/settings/


TAILWIND_CLI_VERSION = "3.4.11"
TAILWIND_CLI_PATH = BASE_DIR / "bin"
TAILWIND_CLI_SRC_CSS = _scoreboard_app_path / "static-src" / "css" / "main.css"
TAILWIND_CLI_DIST_CSS = "css/main.css"
