import jwt

from nanohttp import settings, HTTPForbidden


class JWTPrincipal:
    """
    Role based JWT Principal
    """
    def __init__(self, payload=None):
        self.payload = payload

    def dump(self) -> str:
        return jwt.encode(
            payload=self.payload,
            key=settings.auth.jwt_secret_key,
            algorithm=settings.auth.jwt_algorithm
        ).decode('utf8')

    def load(self, token: str):
        self.payload = jwt.decode(
            token,
            key=settings.auth.jwt_secret_key,
            algorithms=settings.auth.jwt_algorithm
        )
        return self

    def to_dict(self):
        return self.payload

    @property
    def roles(self):
        return self.payload.get('roles')

    def is_in_roles(self, *roles):
        if self.payload.get('roles'):
            if set(self.payload['roles']).intersection(roles):
                return True
        return False

    def assert_roles(self, *roles):
        if roles and not self.is_in_roles(*roles):
            raise HTTPForbidden

    @property
    def id(self):
        return int(self.payload.get('id'))

    @property
    def session_id(self):
        return self.payload.get('sessionId')


class DefaultJWTPrincipal(JWTPrincipal):

    @property
    def email(self):
        return self.payload.get('email')

    @property
    def mobile(self):
        return self.payload.get('mobile')
