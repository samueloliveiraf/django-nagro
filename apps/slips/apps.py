from django.apps import AppConfig


class SlipsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.slips'

    def ready(self):
        import apps.slips.signals
