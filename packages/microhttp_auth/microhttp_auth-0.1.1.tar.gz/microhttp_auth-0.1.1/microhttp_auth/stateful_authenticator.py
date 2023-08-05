
import re
import ujson
import redis
import user_agents

from datetime import datetime

from nanohttp import context, settings

from .authenticator import Authenticator


class StatefulAuthenticator(Authenticator):
    """
    Stateful Authenticator

    (modified version of RestfulPy Authenticator)

     Redis data-model:
        sessions: HashMap { session_id: member_id }
        member_id: Set { session_id }
        agents: HashMap {
          session_id: {
            remoteAddress: 127.0.0.1,
            machine: pc,
            os: android 4.2.2,
            agent: chrome 55,
            client: MicrohttpClient-js 3.4.5-alpha14,
            lastActivity: 2015-10-26T07:46:36.615661
          }
        }
    """
    _redis = None
    remote_address_key = 'REMOTE_ADDR'
    agent_key = 'HTTP_USER_AGENT'
    client_name = 'MicrohttpClient'
    members_key = 'auth:member:%s'
    sessions_key = 'auth:sessions'
    session_info_key = 'auth:sessions:%s:info'

    @staticmethod
    def create_blocking_redis_client():
        return redis.StrictRedis(
            host=settings.auth.redis.host,
            port=settings.auth.redis.port
        )

    @property
    def redis(self):
        if self.__class__._redis is None:
            self.__class__._redis = self.create_blocking_redis_client()
        return self.__class__._redis

    @classmethod
    def get_member_sessions_key(cls, member_id):
        return cls.members_key % member_id

    @classmethod
    def get_session_info_key(cls, session_id):
        return cls.session_info_key % session_id

    def extract_session_info(self):
        remote_address = machine = os = agent = client = app = None

        if (
            self.remote_address_key in context.environ and
            context.environ[self.remote_address_key]
        ):
            remote_address = context.environ[self.remote_address_key]

        if self.agent_key in context.environ:
            agent_string = context.environ[self.agent_key]
            user_agent = user_agents.parse(agent_string)

            machine = user_agent.is_pc and 'PC' or user_agent.device.family
            os = ' '.join([
                user_agent.os.family,
                user_agent.os.version_string
            ]).strip()
            agent = ' '.join([
                user_agent.browser.family,
                user_agent.browser.version_string
            ]).strip()

            matched_client = re.match(
                '.*%s-(?P<type>.+)/(?P<version>.+) \\((?P<features>.+)\\).*'
                % self.client_name,
                agent_string
            )
            if matched_client:
                matched_client = matched_client.groupdict()
                client_type = matched_client['type']
                client_version = matched_client['version']
                # exp: "Microhttp-js 1.2.3-rc10"
                client = f'{self.client_name}-{client_type} {client_version}'

                features = matched_client['features'].split(';')
                if len(features) >= 3:
                    # exp: "MobileToken (shark) 1.2.3"
                    app = '%s (%s) %s' % (
                        features[0].strip(),
                        features[1].strip(),
                        features[2].strip(),
                    )

        return {
            'remoteAddress': remote_address or 'NA',
            'machine': machine or 'Other',
            'os': os or 'Other',
            'agent': agent or 'Other',
            'client': client or 'Unknown',
            'app': app or 'Unknown',
            'lastActivity': datetime.utcnow().isoformat()
        }

    def update_session_info(self, session_id):
        self.redis.set(
            self.get_session_info_key(session_id),
            ujson.dumps(self.extract_session_info())
        )

    def register_session(self, member_id, session_id):
        self.redis.hset(self.sessions_key, session_id, member_id)
        self.redis.sadd(self.get_member_sessions_key(member_id), session_id)
        self.redis.set(
            self.get_session_info_key(session_id),
            ujson.dumps(self.extract_session_info())
        )

    def unregister_session(self, session_id=None):
        session_id = session_id or context.identity.session_id
        member_id = self.redis.hget(self.sessions_key, session_id)
        self.redis.srem(self.get_member_sessions_key(member_id), session_id)
        self.redis.hdel(self.sessions_key, session_id)
        self.redis.delete(self.get_session_info_key(session_id))

    def validate_session(self, session_id):
        return self.redis.hexists(self.sessions_key, session_id)

    def invalidate_member(self, member_id=None):
        """ Remove member all sessions """
        while True:
            session_id = self.redis.spop(
                self.get_member_sessions_key(member_id)
            )
            if not session_id:
                break
            self.redis.hdel(self.sessions_key, session_id)
            self.redis.delete(self.get_session_info_key(session_id))
        self.redis.delete(self.get_member_sessions_key(member_id))

    def authenticate_request(self):
        super().authenticate_request()
        if not context.identity:
            return

        if not self.validate_session(context.identity.session_id):
            context.identity = None
            return

        self.update_session_info(context.identity.session_id)

    def get_member_sessions(self, member_id: int):
        return list(map(
            lambda x: x.decode(),
            self.redis.smembers(self.get_member_sessions_key(member_id))
        ))

    def get_session_info(self, session_id):
        info = self.redis.get(self.get_session_info_key(session_id))
        if info:
            return ujson.loads(info)
        return None
