from flask_philo_pynamodb import resolv_environment

from pynamodb.constants import REGION, HOST
from pynamodb.connection.table import TableConnection
from pynamodb.models import Model


class FlaskPynamoDBModel(Model):

    @classmethod
    def _get_connection(cls):
        """
        Append attributes to Metaclass if they are defined
        in The Flask-Philo-Core configuration object.
        """
        env = resolv_environment()

        setattr(cls.Meta, HOST, env.get(HOST))

        if not hasattr(cls.Meta, REGION):
            setattr(cls.Meta, REGION, env.get('AWS_REGION'))

        if not hasattr(cls.Meta, 'request_timeout_seconds'):
            setattr(
                cls.Meta, 'request_timeout_seconds',
                env.get('request_timeout_seconds'))

        if not hasattr(cls.Meta, 'base_backoff_ms'):
            setattr(cls.Meta, 'base_backoff_ms', env.get('base_backoff_ms'))

        if not hasattr(cls.Meta, 'max_retry_attempts'):
            setattr(
                cls.Meta, 'max_retry_attempts', env.get('max_retry_attempts'))

        if not hasattr(cls.Meta, 'aws_access_key_id'):
            setattr(
                cls.Meta, 'aws_access_key_id', env.get('AWS_ACCESS_KEY_ID'))
        elif not cls.Meta.aws_access_key_id:
            setattr(
                cls.Meta, 'aws_access_key_id', env.get('AWS_ACCESS_KEY_ID'))

        if not hasattr(cls.Meta, 'aws_secret_access_key'):
            setattr(
                cls.Meta, 'aws_secret_access_key',
                env.get('AWS_SECRET_ACCESS_KEY'))

        elif not cls.Meta.aws_secret_access_key:
            setattr(
                cls.Meta,
                'aws_secret_access_key',
                env.get('AWS_SECRET_ACCESS_KEY'))

        if not hasattr(cls.Meta, 'session_cls'):
            setattr(cls.Meta, 'session_cls', env.get('session_cls'))

        cls._connection = TableConnection(
            cls.Meta.table_name,
            region=cls.Meta.region,
            host=cls.Meta.host,
            session_cls=cls.Meta.session_cls,
            request_timeout_seconds=cls.Meta.request_timeout_seconds,
            max_retry_attempts=cls.Meta.max_retry_attempts,
            base_backoff_ms=cls.Meta.base_backoff_ms,
            aws_access_key_id=cls.Meta.aws_access_key_id,
            aws_secret_access_key=cls.Meta.aws_secret_access_key)

        return cls._connection
