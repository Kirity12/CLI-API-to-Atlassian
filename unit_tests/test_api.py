import sys
import os
import pytest
from unittest.mock import Mock
import json
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from trello_cli_service.trello_api import TrelloApi
import requests

API_KEY = "26dea0c6d8f4574827f3e06654ab5102"
TOKEN_KEY = "ATTA0c9670fe99c679e661aeef28cd9275b160270a70dff5e00fc4cd516fe1f321ef059D598F"
COL_ID = '6503765a250478954fb2c0f2'


def mock_response(status_code, json_data):
    response = Mock()
    response.status_code = status_code
    response.text = json_data
    return response


@pytest.fixture(scope="session")
def trello_api_instance():
    return TrelloApi(apikey=API_KEY, token=TOKEN_KEY)

 
def test_add_card(trello_api_instance):

    name = "Test Card 1"
    desc = "Test description 1"
    
    dd = json.dumps({'idList': COL_ID})
    requests.request = Mock(return_value=mock_response(200, dd))
    
    status, text = trello_api_instance.add_card(name, COL_ID, desc)

    assert status == 200
    assert text['idList'] == COL_ID
