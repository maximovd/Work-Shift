# -*- coding: utf-8 -*

import os
import pytest

from app import create_app


@pytest.fixture(scope='module')
def flask_client():
    flask_app = create_app()
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'TEST_DATABASE_URL',
    )
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_SCRF_ENABLED'] = False
    flask_app.config['UPLOADS_DIRECTORY'] = os.path.join(
        os.path.dirname(__file__),
        '..',
        'app',
        'static',
        'uploads',
        '',
    )
    client = flask_app.test_client()

    with flask_app.app_context():
        yield client
