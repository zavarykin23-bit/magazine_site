from pathlib import Path
import os
import logging

try:
    from dotenv import load_dotenv
except Exception:  
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent.parent

if load_dotenv is not None:
    load_dotenv(BASE_DIR / '.env')
    load_dotenv(BASE_DIR.parent / '.env')

SECRET_KEY = 'django-insecure-your-secret-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'requests_app.views': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'requests_app',  
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fish_day_admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fish_day_admin.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_DIRS = []
if os.path.exists(os.path.join(BASE_DIR, 'static')):
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'рыбный день')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

RATELIMIT_ENABLE = True
RATELIMIT_PER_IP = 5


def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST_USER = (os.getenv('EMAIL_HOST_USER', '') or '').strip()
EMAIL_HOST_PASSWORD = (os.getenv('EMAIL_HOST_PASSWORD', '') or '').strip()

_email_host_env = os.getenv('EMAIL_HOST')
_email_port_env = os.getenv('EMAIL_PORT')
_email_use_tls_env = os.getenv('EMAIL_USE_TLS')
_email_use_ssl_env = os.getenv('EMAIL_USE_SSL')

_email_user_l = EMAIL_HOST_USER.lower()
_email_provider = 'yandex'
if _email_user_l.endswith(('@mail.ru', '@inbox.ru', '@bk.ru', '@list.ru', '@internet.ru')):
    _email_provider = 'mailru'
elif _email_user_l.endswith(('@gmail.com', '@googlemail.com')):
    _email_provider = 'gmail'

if _email_provider == 'mailru':
    _default_email_host = 'smtp.mail.ru'
    _default_email_port = 465
    _default_email_use_tls = False
    _default_email_use_ssl = True
elif _email_provider == 'gmail':
    _default_email_host = 'smtp.gmail.com'
    _default_email_port = 587
    _default_email_use_tls = True
    _default_email_use_ssl = False
else:
    _default_email_host = 'smtp.yandex.ru'
    _default_email_port = 465
    _default_email_use_tls = False
    _default_email_use_ssl = True

EMAIL_HOST = (_email_host_env or _default_email_host).strip()
EMAIL_PORT = int((_email_port_env or str(_default_email_port)).strip())
EMAIL_USE_TLS = _env_bool('EMAIL_USE_TLS', _default_email_use_tls) if _email_use_tls_env is not None else _default_email_use_tls
EMAIL_USE_SSL = _env_bool('EMAIL_USE_SSL', _default_email_use_ssl) if _email_use_ssl_env is not None else _default_email_use_ssl
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '20'))


_email_host_l = (EMAIL_HOST or '').strip().lower()
if _email_user_l.endswith(('@yandex.ru', '@yandex.com', '@ya.ru')) and 'mail.ru' in _email_host_l:
    logging.getLogger(__name__).warning(
        'EMAIL_HOST was mail.ru while EMAIL_HOST_USER is Yandex; switched to smtp.yandex.ru'
    )
    EMAIL_HOST = 'smtp.yandex.ru'
elif _email_user_l.endswith(('@mail.ru', '@inbox.ru', '@bk.ru', '@list.ru', '@internet.ru')) and 'yandex' in _email_host_l:
    logging.getLogger(__name__).warning(
        'EMAIL_HOST was Yandex while EMAIL_HOST_USER is Mail.ru; switched to smtp.mail.ru'
    )
    EMAIL_HOST = 'smtp.mail.ru'
    if _email_port_env is None:
        EMAIL_PORT = 465
    if _email_use_tls_env is None:
        EMAIL_USE_TLS = False
    if _email_use_ssl_env is None:
        EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = DEFAULT_FROM_EMAIL
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', EMAIL_HOST_USER)

if EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        logging.getLogger(__name__).warning(
            'SMTP is enabled but EMAIL_HOST_USER/EMAIL_HOST_PASSWORD are missing. Emails will not be sent.'
        )
    elif EMAIL_HOST == 'smtp.yandex.ru' and EMAIL_HOST_USER.lower().endswith('@yandex.com'):
        logging.getLogger(__name__).warning(
            'Using @yandex.com with smtp.yandex.ru may fail. Prefer mailbox login @yandex.ru (or exact mailbox domain).'
        )
