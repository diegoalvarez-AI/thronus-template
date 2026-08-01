from .settings import *  # noqa: F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Desabilita whitenoise em testes — não precisa de arquivos estáticos
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
