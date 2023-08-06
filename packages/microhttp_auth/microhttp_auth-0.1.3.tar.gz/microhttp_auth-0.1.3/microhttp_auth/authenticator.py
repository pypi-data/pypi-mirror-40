import jwt
import functools

from typing import Union

from nanohttp import context, HTTPForbidden, HTTPUnauthorized, HTTPBadRequest

from microhttp_auth import JWTPrincipal, DefaultJWTPrincipal


class Authenticator:
    header_token_key = 'HTTP_AUTHORIZATION'
    __jwt_principal__ = DefaultJWTPrincipal

    @classmethod
    def create_token(cls, payload: dict):
        return JWTPrincipal(payload).dump()

    def get_principal(self) -> Union[None, JWTPrincipal]:
        # noinspection PyBroadException
        try:
            return self.__class__.__jwt_principal__().load(
                context.environ[self.header_token_key]
            )
        except jwt.InvalidTokenError:
            pass

    def authenticate_request(self):
        context.identity = None
        if self.header_token_key not in context.environ:
            return

        encoded_token = context.environ[self.header_token_key]
        if encoded_token is None or not encoded_token.strip():
            return

        context.identity = self.get_principal()
        if not context.identity:
            raise HTTPBadRequest


def authorize(*roles):
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            if not context.identity:
                raise HTTPUnauthorized('No identity')

            if len(roles) > 0 and not context.identity.is_in_roles(*roles):
                raise HTTPForbidden

            return func(*args, **kwargs)

        return wrapper

    if roles and callable(roles[0]):
        f = roles[0]
        roles = []
        return decorator(f)
    else:
        return decorator
