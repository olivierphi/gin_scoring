import os

os.environ["NO_DOT_ENV"] = "YES"

from ._base import *

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DEBUG = False

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Static assets served by Whitenoise on production
# @link https://devcenter.heroku.com/articles/django-assets
# @link http://whitenoise.evans.io/en/stable/
STATIC_ROOT = BASE_DIR / "staticfiles"
MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
