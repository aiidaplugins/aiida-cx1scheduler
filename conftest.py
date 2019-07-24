import os
from aiida.manage.fixtures import fixture_manager
import pytest


@pytest.fixture(scope='session')
def aiida_environment():
    """setup a test profile for the duration of the tests"""
    # TODO this is required locally for click
    # (see https://click.palletsprojects.com/en/7.x/python3/)
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    with fixture_manager() as fixture_mgr:
        yield fixture_mgr


@pytest.fixture(scope='function')
def new_database(aiida_environment):
    """Get a database for the test and clean it up after it finishes"""
    aiida_environment.reset_db()
    return
