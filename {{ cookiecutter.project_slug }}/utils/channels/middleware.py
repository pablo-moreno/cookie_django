from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from utils.channels.users import get_user_by_token


class TokenAuthMiddleware(object):
    """
    Custom middleware that sets the user from a given token.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        qs = parse_qs(scope["query_string"].decode("utf-8"))
        token = qs.get("token")[0]
        scope["user"] = await get_user_by_token(token)

        return await self.app(scope, receive, send)


def token_auth_middleware_stack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
