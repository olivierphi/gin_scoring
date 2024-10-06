from django.apps import AppConfig

# N.B. "auth" is already used by Django, so let's use the long form 😅


class AuthenticationAppConfig(AppConfig):
    name = "gin_scoring.apps.authentication"
