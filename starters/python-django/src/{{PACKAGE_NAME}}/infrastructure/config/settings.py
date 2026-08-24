import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _require_env(var: str) -> str:
    value = os.environ.get(var)
    if not value:
        raise ImproperlyConfigured(f"Variável de ambiente obrigatória não definida: {var}")
    return value


DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"

_secret_env = os.environ.get("SECRET_KEY", "")
if _secret_env:
    SECRET_KEY = _secret_env
elif DEBUG:
    SECRET_KEY = "django-insecure-dev-only-NOT-para-producao"
else:
    raise ImproperlyConfigured("SECRET_KEY deve ser definida em produção.")

_allowed_env = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in _allowed_env.split(",") if h.strip()]
if not ALLOWED_HOSTS:
    if DEBUG:
        ALLOWED_HOSTS = ["*"]
    else:
        raise ImproperlyConfigured("ALLOWED_HOSTS deve ser definida em produção.")

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h != "*"]

INSTALLED_APPS = [
    "persistence.apps.PersistenceConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _require_env("POSTGRES_DB"),
        "USER": _require_env("POSTGRES_USER"),
        "PASSWORD": _require_env("POSTGRES_PASSWORD"),
        "HOST": _require_env("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "OPTIONS": {"connect_timeout": 5},
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
    }
}

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 28800
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 63072000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{asctime} [{levelname}] {name}: {message}", "style": "{", "datefmt": "%Y-%m-%d %H:%M:%S"},
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "verbose"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "django": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "{{PACKAGE_NAME}}": {"handlers": ["console"], "level": "DEBUG" if DEBUG else "INFO", "propagate": False},
    },
}

_sentry_dsn = os.environ.get("SENTRY_DSN", "")
if _sentry_dsn:
    try:
        import logging
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
        sentry_sdk.init(
            dsn=_sentry_dsn,
            integrations=[
                DjangoIntegration(transaction_style="url"),
                LoggingIntegration(level=logging.WARNING, event_level=logging.ERROR),
            ],
            traces_sample_rate=0.05,
            send_default_pii=False,
            environment="development" if DEBUG else "production",
            release=os.environ.get("APP_RELEASE", "unknown"),
        )
    except ImportError:
        pass
