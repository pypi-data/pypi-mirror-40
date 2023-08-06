from flask import current_app
from flask_philo_core import ConfigurationError
from pynamodb.constants import REGION, HOST
from pynamodb.settings import get_settings_value

import os

__verson__ = '0.1.0'


def resolv_environment():
    """
    AWS configuration parameters such as AWS credentials
    can de defined by using environ variables or
    configuration file. PyNAMoDb settings should be
    defined in the configuration file
    """

    attrs = {}
    app = current_app._get_current_object()
    aws_config = app.config.get('AWS', {})
    pynamo_config = app.config.get('PYNAMODB', {})

    if 'AWS_REGION' in aws_config:
        attrs['AWS_REGION'] = aws_config['AWS_REGION']

    elif 'AWS_REGION' in os.environ:
        attrs['AWS_REGION'] = os.environ['AWS_REGION']
    else:
        attrs['AWS_REGION'] = get_settings_value(REGION)

    if 'AWS_ACCESS_KEY_ID' in aws_config:
        attrs['AWS_ACCESS_KEY_ID'] = aws_config['AWS_ACCESS_KEY_ID']

    elif 'AWS_ACCESS_KEY_ID' in os.environ:
        attrs['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']

    else:
        raise ConfigurationError('AWS_ACCESS_KEY_ID undefined')

    if 'AWS_SECRET_ACCESS_KEY' in aws_config:
        attrs['AWS_SECRET_ACCESS_KEY'] = aws_config['AWS_SECRET_ACCESS_KEY']

    elif 'AWS_ACCESS_KEY_ID' in os.environ:
        attrs['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']

    else:
        raise ConfigurationError('AWS_SECRET_ACCESS_KEY undefined')

    if HOST in pynamo_config:
        attrs[HOST] = pynamo_config[HOST]
    else:
        attrs[HOST] = get_settings_value('host')

    if 'request_timeout_seconds' in pynamo_config:
        attrs['request_timeout_seconds'] =\
            pynamo_config['request_timeout_seconds']
    else:
        attrs['request_timeout_seconds'] =\
            get_settings_value('request_timeout_seconds')

    if 'base_backoff_ms' in pynamo_config:
        attrs['base_backoff_ms'] = pynamo_config['base_backoff_ms']
    else:
        attrs['base_backoff_ms'] = get_settings_value('base_backoff_ms')

    if 'max_retry_attempts' in pynamo_config:
        attrs['max_retry_attempts'] = pynamo_config['max_retry_attempts']
    else:
        attrs['max_retry_attempts'] = get_settings_value('max_retry_attempts')

    if 'session_cls' in pynamo_config:
        attrs['session_cls'] = pynamo_config['session_cls']
    else:
        attrs['session_cls'] = get_settings_value('session_cls')

    return attrs
