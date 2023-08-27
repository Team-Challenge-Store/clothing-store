"""Unit tests for the API"""

import logging

from app import app


def test_valid_post_request_to_register_user():
    """
    Test a valid POST request to register a user with proper data.

    Returns:
        None
    """

    with app.test_client() as client:

        data={'username': 'testing',
         'email': 'testing@gmail.com',
         'password': 'Tes123!',
         'repeat_password': 'Tes123!'}
        

        response = client.post('/register', json=data)

        logging.info(response.json)

        assert response.status_code == 201


def test_unvalid_post_request_to_register_user():
    """
    Test an invalid POST request to register a user with missing data.

    Returns:
        None
    """

    with app.test_client() as client:

        data={'username': '',
         'email': '',
         'password': '',
         'repeat_password': ''}

        response = client.post('/register', json=data)
        logging.info(response.json)

        assert response.status_code == 400


def test_valid_requests_to_login_user():
    """
    Test a valid GET and POST requests to login a user with proper data
    Returns None
    """

    with app.test_client() as client:

        data={'email':'testing@gmail.com',
              'password':'Tes123!'}
        
        response = client.get('/login')
        assert response.status_code == 200

        response = client.post('/login', json=data)
        logging.info(response.json)

        assert response.status_code == 200


def test_invalid_post_request_to_login_user():
    """
    Test an invalid POST request to login a user with wrong data
    Returns None
    """
    
    with app.test_client() as client:

        data={'email': 'wrong@gmail.com',
              'password': 'password'}
        
        response = client.post('/login', json=data)
        logging.info(response.json)

        assert response.status_code == 401

def test_get_request_to_logout_user():
    """
    Test a valid GET request to logout a user
    Returns None
    """

    with app.test_client() as client:

        response = client.get('/logout')
        assert response.status_code == 200
