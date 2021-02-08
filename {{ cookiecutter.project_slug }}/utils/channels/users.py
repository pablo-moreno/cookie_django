from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user_by_token(token):
    token = Token.objects.filter(key=token)

    if not token.exists():
        return AnonymousUser()

    return token.first().user
