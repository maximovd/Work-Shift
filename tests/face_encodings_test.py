# -*- coding: utf-8 -*

from flask import current_app
from app.models import face_encoding_image


def test_create_face_encondings(flask_client):
    empty_list = []
    destination = ''.join(
        [
            current_app.config['UPLOADS_DIRECTORY'],
            'test_image.jpeg',
        ],
    )

    encodings = face_encoding_image(destination=destination)
    assert encodings != empty_list
    assert isinstance(encodings, list)
