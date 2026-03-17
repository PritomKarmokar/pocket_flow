import os
import environ

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env_file_path = os.path.join(BASE_DIR, ".env")
env.read_env(env_file_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third Party Apps
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'cid.apps.CidAppConfig',
]

# ADD In House Project Apps Here
PROJECT_APPS = [
    'authentication',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'cid.middleware.CidMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pocket_flow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pocket_flow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.str('DB_PORT'),
        'OPTIONS': env.dict('DB_OPTIONS'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "authentication.User"

# Django-correlation-id Config
CID_GENERATE = True
CID_HEADER = 'HTTP_X_REQUEST_ID'
CID_RESPONSE_HEADER = 'X-Request-ID'
# Django-correlation-id Config End

# LOGGING SETUP START #
LOG_LEVEL = env.str('LOG_LEVEL', 'DEBUG')
LOGGER_ROOT_NAME = env.str("LOGGER_ROOT_NAME", "pocket_flow")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[cid: {cid}] | {asctime} | {levelname} | {pathname}:{lineno} | {message}',
            'style': '{',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'filters': ['correlation'],
        },
    },
    'filters': {
        'correlation': {
            '()': 'cid.log.CidContextFilter'
        },
    },
    'loggers': {
        LOGGER_ROOT_NAME: {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
            'filters': ['correlation'],
        },

        'general': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },

    },
}
# LOG config end

REQUEST_TIMEOUT = env.int("REQUEST_TIMEOUT", 30)
SERVICE_NAME = env.str("SERVICE_NAME", "pocket-flow")

# CORS CONFIG
CORS_ALLOW_ALL_ORIGINS = True

# note: Set `CORS_ALLOW_ALL_ORIGINS` to `False` if production environment and configure `CORS_ALLOWED_ORIGINS` and `CORS_ALLOW_CREDENTIALS` based on your requirements :)

# CORS_ALLOWED_ORIGINS = [
#     "https://frontend.yourdomain.com",
# ]
#
# CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
    'PATCH',
)
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'contenttype',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
# CORS CONFIG END #

# JWT Authentication Setup
JWT_ALGORITHM = env.str("JWT_ALGORITHM")
JWT_VERIFYING_KEY = env.str("JWT_VERIFYING_KEY")
JWT_AUDIENCE = env.str("JWT_AUDIENCE")
JWT_ISSUER = env.str("JWT_ISSUER")
JWT_AUTH_HEADER_TYPES = env.list('JWT_AUTH_HEADER_TYPES')
# JWT Authentication Setup End

# Simple JWT settings start
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "TOKEN_BLACKLIST_ENABLED": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": JWT_ALGORITHM,
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": JWT_VERIFYING_KEY,
    "AUDIENCE": JWT_AUDIENCE,
    "ISSUER": JWT_ISSUER,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": JWT_AUTH_HEADER_TYPES,
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}
# Simple JWT settings end

# Google OAuth Config
GOOGLE_CLIENT_ID = env.str('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = env.str('GOOGLE_CLIENT_SECRET')
# Google OAuth Config End