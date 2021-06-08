from __future__ import absolute_import, unicode_literals

import pytest

from unittest.mock import patch

from celery.contrib.pytest import depends_on_current_app
from celery.contrib.testing.app import TestApp, Trap

__all__ = ['app', 'depends_on_current_app']


@pytest.fixture(scope='session', autouse=True)
def setup_default_app_trap():
    from celery._state import set_default_app
    set_default_app(Trap())


@pytest.fixture()
def app(celery_app):
    return celery_app


@patch('request.instance.app')
@patch('request.instance.Celery')
@patch('request.instance.add')
@pytest.fixture(autouse=True)
def test_cases_shortcuts(request, app):
    if request.instance:
        @app.task
        def add(x, y):
            return x + y

        # IMPORTANT: We set an .app attribute for every test case class.
        request.instance.app = app
        request.instance.Celery = TestApp
        request.instance.add = add
    yield
    if request.instance:
        request.instance.app = None
