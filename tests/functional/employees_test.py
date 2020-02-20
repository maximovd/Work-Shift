STATUS_CODE_OK = 200
STATUS_CODE_FOUND = 302


def test_add_page(init_client):
    response = init_client.get('/add')
    assert response.status_code == STATUS_CODE_FOUND


def test_browse_page(init_client):
    response = init_client.get('/browse')
    assert response.status_code == STATUS_CODE_FOUND
