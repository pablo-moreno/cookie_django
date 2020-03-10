from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token


class TokenMiddleware(BaseMiddleware):
    """
        Middleware to populate django user to the scope using the token passed in the query_string
    """

    def populate_scope(self, scope):
        qs = parse_qs(scope['query_string'].decode('utf-8'))
        token = qs.get('token')

        if not token:
            raise ValueError('Token not found')

        token = Token.objects.get(key=token)
        user = token.user

        scope['user'] = user

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = scope.get('user')
