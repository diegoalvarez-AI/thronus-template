from django.apps import AppConfig


class PersistenceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "persistence"
    label = "persistence"
    verbose_name = "{{PROJECT_NAME}}"
