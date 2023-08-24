from pathlib import Path
from decouple import config

# Environment Settings:
TIME_ZONE = config("TIME_ZONE", default="UTC")
DEBUG = config("DEBUG", cast=bool, default=True)
SECRET_KEY = config("API_SECRET_KEY", default="development_secret_key")
ALLOWED_HOSTS = ["*"] if DEBUG else config(
    "ALLOWED_HOSTS",
    cast=lambda hosts: [host_ip.strip() for host_ip in hosts.split(",")]
)

# Basic Configs:
LANGUAGE_CODE = 'en-us'
ROOT_URLCONF = 'config.urls'
ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = 'config.wsgi.application'
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
BASE_DIR = Path(__file__).resolve().parent.parent
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# REST Framework Configs:
REST_FRAMEWORK = {
    "PAGE_SIZE": 10,
}

# Mode Handling:
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

    # Cache Services:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

    # Development sqlite db :
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    # Email settings
    EMAIL_USE_TLS = False
    EMAIL_HOST = "localhost"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 25
else:
    # Cache Services:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": config("REDIS_URL"),
        }
    }

    # Email settings
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=True)
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@example.com")

    # CORS engine configuration (django-cors-headers) :
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = config(
        "CORS_ALLOWED_ORIGINS",
        cast=lambda origins: [origin.strip() for origin in origins.split(",")],
        default="http://0.0.0.0:8000, http://localhost:8000",
    )

    # Production postgresql db :
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT", cast=int),
        },
    }

    # Django's SSL security configurations :
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)

    # Https settings
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = "HTTP_X_FORWARDED_PROTO", "https"

    # HSTS settings
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 86400

    # more security settings
    USE_X_FORWARDED_HOST = True
    SECURE_REFERRER_POLICY = "strict-origin"

    # Static directories:
    # STATICFILES_DIRS = [BASE_DIR / "main/build/static"]

# Internationalization Configs:
USE_TZ = True
USE_L10 = True
USE_L10N = True
USE_I18N = True

# Serving Configs:
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"

# Basic Security Configs
X_FRAME_OPTIONS = "SAMEORIGIN"
SESSION_TIMEOUT = 24 * 60 * 60
SESSION_COOKIE_AGE = 3 * 60 * 60
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Content Security Policy
CSP_DEFAULT_SRC = "'none'",
CSP_STYLE_SRC = "'self'",
CSP_SCRIPT_SRC = "'self'",
CSP_IMG_SRC = "'self'",
CSP_FONT_SRC = "'self'",

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Password validation
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

# Celery Configs:
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = 'json',
CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://:@localhost:6379/0")
CELERY_BROKER_BACKEND = config("CELERY_BROKER_BACKEND", default="redis://:@localhost:6379/1")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://:@localhost:6379/2")
