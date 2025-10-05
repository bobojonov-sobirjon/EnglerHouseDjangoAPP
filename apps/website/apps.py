from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.website'
    verbose_name = 'Управление сайтом'
    
    def ready(self):
        import apps.website.signals