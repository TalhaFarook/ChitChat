from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Set the name of the app.
    name = 'apps.user'
