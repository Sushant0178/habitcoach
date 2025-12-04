from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  #----- this line added
    name = 'accounts'

    def ready(self):   #---- this method added
        import accounts.signals
