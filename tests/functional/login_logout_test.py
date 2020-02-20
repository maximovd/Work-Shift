from app.models import User


def test_login(init_client):
    user = User(username='test_admin', email='test@test.com')
    password = user.set_password('123456')
    response = init_client(
        '/login',
        data={
            'username': 'test_admin',
            'password': password,
        },
        follow_redirect=True,
    )
    assert response.status_code == 200