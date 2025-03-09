import pytest
import src.services as services
from unittest import mock
import requests

@mock.patch('src.services.get_users_from_db')
def test_get_users_from_db(mock_get_users_from_db):
    mock_get_users_from_db.return_value = 'Mocked Data'

    username = services.get_users_from_db(1)

    assert username=='Mocked Data'

@mock.patch('requests.get')
def test_get_users_from_api(mock_get_users_from_api):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "1", "name": "Sohail"}

    mock_get_users_from_api.return_value = mock_response
    user = services.get_users_from_api()

    assert user == {"id": "1", "name": "Sohail"}

@mock.patch('requests.get')
def test_get_users_from_api_error(mock_get_users_from_api):
    mock_response = mock.Mock()
    mock_response.status_code = 400

    mock_get_users_from_api.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        services.get_users_from_api()


# mock job data, applicant data,
# write all the test case methods.
# 