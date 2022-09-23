from .production import *


CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# We let Fly.io make sure that we're using HTTPS, and disable these settings as the Docker container won't
# have enough knowledge of the HTTP layer to be able to check these things:
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
