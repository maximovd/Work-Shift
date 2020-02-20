import os
import pytest

from app import create_app, db
from app.models import User


@pytest.fixture(scope='module')
def init_database():
    flask_app = create_app()
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'TEST_DATABASE_URL',
    )
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_SCRF_ENABLED'] = False
    with flask_app.app_context():
        db.create_all()
        user = User(username='test_admin', email='test@test.com')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        yield db
        db.drop_all()


@pytest.fixture(scope='module')
def init_client():
    flask_app = create_app()
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'TEST_DATABASE_URL',
    )
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_SCRF_ENABLED'] = False
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()