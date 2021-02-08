from .base import *

DOMAIN = '{{ cookiecutter.dev_domain }}'
BASE_URL = f'https://{DOMAIN}'

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

DEV_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]

MIDDLEWARE = DEV_MIDDLEWARE + MIDDLEWARE
