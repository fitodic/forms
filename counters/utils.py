# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from redis import StrictRedis


def redis_is_active():
    """Check the status of Redis."""
    if hasattr(settings, 'USE_REDIS'):
        return settings.USE_REDIS
    else:
        return False


def get_connection():
    """Create a Redis connection."""

    host = settings.REDIS_CONNECTION.get('host')
    port = settings.REDIS_CONNECTION.get('port')
    db = settings.REDIS_CONNECTION.get('db')

    return StrictRedis(host=host, port=port, db=db)


def flush_db():
    """Delete all keys in the current database."""
    connection = get_connection()
    connection.flushdb()


def increment_by(key, value=1):
    """Increment the value stored under the specified key or create it with the
    default value if the key does not exist.

    Arguments:
        key {str} -- key name
        value {int} -- increment value {default: {1}}
    """
    connection = get_connection()
    connection.incrby(name=key, amount=value)


def get_key_value(key):
    """Return the value stored under the specified key or None if the key does
    not exist.

    Arguments:
        key {str} -- key name
    """
    connection = get_connection()
    return connection.get(key)
