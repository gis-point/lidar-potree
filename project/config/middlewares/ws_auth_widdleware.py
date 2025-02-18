import os
import django
import jwt
from collections import OrderedDict
from datetime import datetime
from typing import Any, Union
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth.models import (
    AnonymousUser,
)
from django.db import close_old_connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(
        self, scope: dict, receive, send
    ) -> Union[ValueError, OrderedDict]:
        if scope["path"] == "/ws/general/":
            return await super().__call__(scope, receive, send)
        else:
            close_old_connections()
            try:
                token_key: str = (
                    dict(
                        (
                            x.split("=")
                            for x in scope["query_string"].decode().split("&")
                        )
                    )
                ).get("token", None)
            except ValueError:
                token_key = None

            return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
