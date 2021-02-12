import os


VERSION = os.environ.get('APP_VERSION')
SECRET_KEY = os.environ.get('SECRET_KEY', 'this-is-the-default-secret-key')
DEBUG = os.environ.get('DEBUG', True) is True

POSTGRES_DB = os.environ.get('POSTGRES_DB', 'postgres')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'postgres')
DATABASE_PORT = os.environ.get('DATABASE_PORT', 5432)
DATABASE_URL = os.environ.get('DATABASE_URL', f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{POSTGRES_DB}')

STATIC_ROOT = os.environ.get('STATIC_ROOT', 'static')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', 'media')

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

PAGE_SIZE = os.environ.get('PAGE_SIZE', 20)

# Minio
USE_MINIO_STORAGE = os.environ.get('USE_MINIO_STORAGE', 'FALSE') == 'TRUE'

if USE_MINIO_STORAGE:
    MINIO_STORAGE_ENDPOINT = os.environ.get('MINIO_STORAGE_ENDPOINT', 's3:9000')
    MINIO_STORAGE_ACCESS_KEY = os.environ.get('MINIO_STORAGE_ACCESS_KEY', 'access_key')
    MINIO_STORAGE_SECRET_KEY = os.environ.get('MINIO_STORAGE_SECRET_KEY', 'secret_key')
    MINIO_STORAGE_USE_HTTPS = os.environ.get('MINIO_STORAGE_USE_HTTPS', 'FALSE') == 'TRUE'
