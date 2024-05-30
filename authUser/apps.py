from django.apps import AppConfig


class AuthuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authUser'
    
    def ready(self):
        try:
            import authUser.signals
        except ImportError:
            raise ImportError("Unable to import signals")
