from django.apps import AppConfig


class DangodbappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DangoDBApp'

    def ready(self):
        import DangoDBApp.signals