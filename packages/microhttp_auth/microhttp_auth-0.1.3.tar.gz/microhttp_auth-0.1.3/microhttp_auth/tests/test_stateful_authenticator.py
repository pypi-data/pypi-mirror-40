import pytest

from uuid import uuid4

from freezegun import freeze_time
from webtest import TestApp as WebtestApp

from nanohttp import Controller, settings, json, context

from microhttp import Application

from microhttp_auth import StatefulAuthenticator, authorize


session_info_test_cases = [
    {
        'environment': {
            'REMOTE_ADDR': '',
            'HTTP_USER_AGENT':
                'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) '
                'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 '
                'Mobile/9B179 Safari/7534.48.3 MicrohttpClient-js/1.2.3 (My '
                'App; test-name; 1.4.5-beta78; fa-IR; some; extra; info)'
        },
        'expected_remote_address': 'NA',
        'expected_machine': 'iPhone',
        'expected_os': 'iOS 5.1',
        'expected_agent': 'Mobile Safari 5.1',
        'expected_client': 'MicrohttpClient-js 1.2.3',
        'expected_app': 'My App (test-name) 1.4.5-beta78',
        'expected_last_activity': '2017-07-13T13:11:44',
    },
    {
        'environment': {
            'REMOTE_ADDR': '185.87.34.23',
            'HTTP_USER_AGENT':
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; '
                'Trident/5.0) MicrohttpClient-custom/4.5.6 (A; B; C)'
        },
        'expected_remote_address': '185.87.34.23',
        'expected_machine': 'PC',
        'expected_os': 'Windows 7',
        'expected_agent': 'IE 9.0',
        'expected_client': 'MicrohttpClient-custom 4.5.6',
        'expected_app': 'A (B) C',
        'expected_last_activity': '2017-07-13T13:11:44',
    },
    {
        'environment': {
            'REMOTE_ADDR': '172.16.0.111',
            'HTTP_USER_AGENT': ''
        },
        'expected_remote_address': '172.16.0.111',
        'expected_machine': 'Other',
        'expected_os': 'Other',
        'expected_agent': 'Other',
        'expected_client': 'Unknown',
        'expected_app': 'Unknown',
        'expected_last_activity': '2017-07-13T13:11:44',
    },
    {
        'environment': {},
        'expected_remote_address': 'NA',
        'expected_machine': 'Other',
        'expected_os': 'Other',
        'expected_agent': 'Other',
        'expected_client': 'Unknown',
        'expected_app': 'Unknown',
        'expected_last_activity': '2017-07-13T13:11:44',
    }
]


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
    def get_payload(self):
        return context.identity.to_dict()

    @json
    def get_session_info(self, session_id: str=None):
        authenticator = StatefulAuthenticator()
        return authenticator.get_session_info(
            session_id or context.identity.session_id
        ) or dict()

    @json
    @authorize
    def terminate_all_sessions(self):
        authenticator = StatefulAuthenticator()
        authenticator.invalidate_member(context.identity.id)
        return dict()

    @json
    @authorize
    def terminate_a_session(self):
        authenticator = StatefulAuthenticator()
        sessions = list(authenticator.get_member_sessions(context.identity.id))
        for session_id in sessions:
            if session_id != context.identity.session_id:
                authenticator.unregister_session(session_id)
        return dict()

    @json
    @authorize
    def get_sessions(self):
        authenticator = StatefulAuthenticator()
        return list(authenticator.get_member_sessions(context.identity.id))

    @json
    def login(self, role_name: str='supervisor'):
        session_id = str(uuid4()).replace('-', '')
        authenticator = StatefulAuthenticator()
        access_token = authenticator.__class__.create_token(dict(
            id=context.form.get('mobile'),
            mobile=context.form.get('mobile'),
            roles=[role_name],
            sessionId=session_id
        ))
        authenticator.register_session(
            member_id=context.form.get('mobile'),
            session_id=session_id
        )
        return dict(
            accessToken=access_token
        )


class MyApplication(Application):

    def __init__(self):
        super().__init__(
            root=RootController()
        )
        self.__authenticator__ = StatefulAuthenticator()

    def configure(self, *args, **kwargs):
        super().configure(*args, **kwargs)
        settings.merge("""
            auth:
              jwt_algorithm: HS256
              jwt_secret_key: DSXdzzxxOiIxMjM0NTY3ODkwIiwFtZSI6IkpvadG4gRG9lrr
              redis:
                host: localhost
                port: 6379
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


@pytest.fixture(scope='module')
def sample_access_token(app):
    resp = app.post('/login/supervisor', params={
        'mobile': '935935935'
    }).json
    return resp['accessToken']


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

    # Empty session info
    resp = app.get('/get_session_info/xyz').json
    assert len(resp.keys()) == 0


@pytest.mark.parametrize('test_case', session_info_test_cases)
def test_sessions_info(app, sample_access_token, test_case):
    with freeze_time("2017-07-13T13:11:44", tz_offset=-4):
        payload = app.get(
            '/get_payload',
            headers={
                'Authorization': sample_access_token
            },
            extra_environ=test_case['environment']
        ).json

        info = app.get('/get_session_info/%s' % payload['sessionId']).json
        expected_info = {
            'remoteAddress': test_case['expected_remote_address'],
            'machine': test_case['expected_machine'],
            'os': test_case['expected_os'],
            'agent': test_case['expected_agent'],
            'client': test_case['expected_client'],
            'app': test_case['expected_app'],
            'lastActivity': test_case['expected_last_activity']
        }

        for info_key, info_val in info.items():
            assert info_val == expected_info[info_key]


def test_manage_sessions(app):
    app.post('/login/operator', params={
        'mobile': '935935936'
    })

    resp = app.post('/login/operator', params={
        'mobile': '935935936'
    }).json
    access_token = resp['accessToken']

    # Get sessions
    sessions = app.get('/get_sessions', headers={
        'Authorization': access_token
    }).json
    assert len(sessions) > 0

    # Terminate one session
    app.delete('/terminate_a_session', headers={
        'Authorization': access_token
    })

    # Terminate all sessions
    app.delete('/terminate_all_sessions', headers={
        'Authorization': access_token
    })

    # Access denied
    app.get('/get_sessions', headers={
        'Authorization': access_token
    }, status=401)


def test_authenticator(app):
    _ = app
    from nanohttp.contexts import Context
    with Context({}):
        authenticator = StatefulAuthenticator()
        member_id = 500

        for session_id in ('bla_bla1', 'bla_bla2', 'bla_bla3'):
            authenticator.register_session(
                member_id=member_id,
                session_id=session_id
            )

            # Get session info
            info = authenticator.get_session_info(
                session_id=session_id
            )
            assert 'remoteAddress' in info

        last_sessions = sessions = authenticator.get_member_sessions(member_id)
        assert len(sessions) >= 0

        authenticator.unregister_session(session_id)

        sessions = authenticator.get_member_sessions(member_id)
        assert len(sessions) == len(last_sessions) - 1

        authenticator.invalidate_member(member_id)

        sessions = authenticator.get_member_sessions(member_id)
        assert len(sessions) == 0
