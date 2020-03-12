STATUS_CODE_OK = 200


def test_login_page(flask_client):
    response = flask_client.get('/auth/login')
    assert response.status_code == STATUS_CODE_OK
