import pytest

from webtest import TestApp as WebtestApp

from nanohttp import Controller, settings, json, context

from microhttp import Application

from microhttp_auth import Authenticator, authorize


class RootController(Controller):

    @json
    @authorize
    def motto(self):
        return dict(
            secret='Draco Dormiens Nunquam Titillandus'
        )

    @json
    @authorize('operator')
    def another_motto(self):
        return dict(
            secret='Titillandus Nunquam Dormiens Draco'
        )

    @json
    @authorize
    def my_identity(self):
        context.identity.assert_roles('operator')
        return dict(
            identity=context.identity.to_dict(),
            roles=context.identity.roles,
            email=context.identity.email,
            mobile=context.identity.mobile
        )

    @json
    def login(self, role_name: str = 'supervisor'):
        authenticator = Authenticator()
        access_token = authenticator.__class__.create_token(dict(
            id=context.form.get('mobile'),
            mobile=context.form.get('mobile'),
            roles=[role_name]
        ))
        return dict(
            accessToken=access_token
        )


class MyApplication(Application):

    def __init__(self):
        super().__init__(
            root=RootController()
        )
        self.__authenticator__ = Authenticator()

    def configure(self, *args, **kwargs):
        super().configure(*args, **kwargs)
        settings.merge("""
            auth:
              jwt_algorithm: HS256
              jwt_secret_key: DSXdzzxxOiIxMjM0NTY3ODkwIiwFtZSI6IkpvadG4gRG9lrr
        """)

    def begin_request(self):
        self.__authenticator__.authenticate_request()

    def prepare(self):
        pass


@pytest.fixture(scope='module')
def app():
    my_app = MyApplication()
    my_app.configure(force=True)
    my_app.prepare()
    return WebtestApp(my_app, lint=False)


def test_authenticate(app):
    # Create access token
    resp = app.post('/login/supervisor', params={
        'mobile': '935935935'
    }).json
    access_token1 = resp['accessToken']

    # Access granted
    app.get('/motto', headers={
        'Authorization': access_token1
    })

    # Access denied
    app.get('/motto', status=401)

    # Create check another role
    resp = app.post('/login/operator', params={
        'mobile': '935935936'
    }).json
    access_token2 = resp['accessToken']

    app.get('/motto', headers={
        'Authorization': access_token2
    })

    app.get('/another_motto', headers={
        'Authorization': access_token2
    })

    app.get('/another_motto', headers={
        'Authorization': access_token1
    }, status=403)

    app.get('/another_motto', status=401)

    app.get('/my_identity', headers={
        'Authorization': access_token2
    })

    app.get('/my_identity', headers={
        'Authorization': access_token1
    }, status=403)

    # Invalid Token
    app.get('/motto', headers={
        'Authorization': 'oh-my-bad'
    }, status=400)

    app.get('/motto', headers={
        'Authorization': None
    }, status=401)

    app.get('/motto', headers={
        'Authorization': '   '
    }, status=401)
