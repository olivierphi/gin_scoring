from .production import *

USE_X_FORWARDED_HOST = True  # Fly.io always sends request through a proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
