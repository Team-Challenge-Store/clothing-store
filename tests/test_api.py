import logging

from app import app


def test_valid_post_request_to_register_user():
    with app.test_client() as client:

        data={'username': 'testing',
         'email': 'testing@gmail.com',
         'password': 'Tes123!',
         'repeat_password': 'Tes123!'}
        

        response = client.post('/register', json=data)

        logging.info(response.json['message'])

        assert response.status_code == 201


def test_unvalid_post_request_to_register_user():
    with app.test_client() as client:

        data={'username': '',
         'email': '',
         'password': '',
         'repeat_password': ''}

        response = client.post('/register', json=data)
        logging.info(response.json)

        assert response.status_code == 400
