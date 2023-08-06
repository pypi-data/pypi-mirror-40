"""
Master file for pytest fixtures.
Any fixtures declared here are available to all test functions in this directory.
"""


import logging

import pytest
from brewblox_service import brewblox_logger, features, service

from brewblox_devcon_spark.__main__ import create_parser

LOGGER = brewblox_logger(__name__)


@pytest.fixture(scope='session', autouse=True)
def log_enabled():
    """Sets log level to DEBUG for all test functions.
    Allows all logged messages to be captured during pytest runs"""
    logging.getLogger().setLevel(logging.DEBUG)
    logging.captureWarnings(True)


@pytest.fixture
def app_config() -> dict:
    return {
        'name': 'test_app',
        'host': 'localhost',
        'port': 1234,
        'debug': True,
        'device_serial': '/dev/TESTEH',
        'device_id': '1234',
        'simulation': False,
        'broadcast_interval': 5,
        'broadcast_exchange': 'brewcast',
        'sync_exchange': 'syncast',
        'mdns_host': '172.17.0.1',
        'mdns_port': 5000,
        'volatile': True,
    }


@pytest.fixture
def sys_args(app_config) -> list:
    return [str(v) for v in [
        'app_name',
        '--debug',
        '--name', app_config['name'],
        '--host', app_config['host'],
        '--port', app_config['port'],
        '--device-serial', app_config['device_serial'],
        '--device-id', app_config['device_id'],
        '--broadcast-interval', app_config['broadcast_interval'],
        '--broadcast-exchange', app_config['broadcast_exchange'],
        '--sync-exchange', app_config['sync_exchange'],
        '--mdns-host', app_config['mdns_host'],
        '--mdns-port', app_config['mdns_port'],
        '--volatile',
    ]]


@pytest.fixture
def app(sys_args):
    parser = create_parser('default')
    app = service.create_app(parser=parser, raw_args=sys_args[1:])
    return app


@pytest.fixture
def client(app, aiohttp_client, loop):
    """Allows patching the app or aiohttp_client before yielding it.

    Any tests wishing to add custom behavior to app can override the fixture
    """
    LOGGER.debug('Available features:')
    for name, impl in app.get(features.FEATURES_KEY, {}).items():
        LOGGER.debug(f'Feature "{name}" = {impl}')
    LOGGER.debug(app.on_startup)

    return loop.run_until_complete(aiohttp_client(app))
