"Define Trello API"
import json
import requests
from requests.utils import quote


class TrelloApi():
    'Performs API requests to Trello for performing various operations'

    def __init__(self, apikey, token=None):
        self._apikey = apikey
        self._token = token
        self.headers = {
                        "Accept": "application/json"
                       }
        self._query = {
                'key': self._apikey,
                'token': self._token
                }
        self.url = "https://api.trello.com/1/"

    def raise_or_json(self, resp):
        "ggat the status code and json response"

        status = resp.status_code
        if status==200:
            obj = json.loads(resp.text)
        else:
            obj = None
        return status, obj

    def set_token(self, token):
        "Set the token"

        self._token = token
        self._query['token'] = token

    def add_card(self, name, col_id, desc=None, id_labels=None):
        "Create new card id along with necessary info json on the given board id"

        url = self.url + "cards"
        query = {
                'key': self._apikey,
                'token': self._token,
                'name': name,
                'desc': desc,
                'idList': col_id,
                'idLabels': id_labels
                }

        response = requests.request(
                                    "POST",
                                    url,
                                    params=query,
                                    headers=self.headers,
                                    timeout=10
                                    )

        return self.raise_or_json(response)

    def add_label_to_card(self, card_id, id_labels):
        "Add label to a card id in the given board id"

        url = self.url + f"cards/{card_id}/idLabels"

        response = requests.request(
                                    "POST",
                                    url,
                                    params=self._query,
                                    headers=self.headers,
                                    data={'value': id_labels},
                                    timeout=10
                                    )

        return self.raise_or_json(response)

    def create_label(self,name, color, id_board):
        "Create new labels json on the given board id"

        url = "https://trello.com/1/labels"

        response = requests.request(
                                    "POST",
                                    url,
                                    params=self._query,
                                    data={"name": name, "color": color, "idBoard": id_board},
                                    timeout=10
                                    )

        return self.raise_or_json(response)

    def get_boards(self):
        "Get Boards json for trello id"

        url = self.url + "/members/me/boards"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self._query,
                                    headers=self.headers,
                                    timeout=10
                                    )

        return self.raise_or_json(response)

    def get_columns(self, board_id):
        "Get Columns json based on the given board id"

        url = self.url + f"boards/{board_id}/lists"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self._query,
                                    headers=self.headers,
                                    timeout=10
                                    )

        return self.raise_or_json(response)

    def get_labels(self, board_id):
        "Get Labels json based on the given board id"

        url = self.url + f"boards/{board_id}/labels"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self._query,
                                    headers=self.headers,
                                    timeout=10
                                    )

        return self.raise_or_json(response)

    def get_cards(self, board_id):
        "Get card json based on the given board id"

        url = self.url + f"boards/{board_id}/cards"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self._query,
                                    headers=self.headers,
                                    timeout=10
                                    )

        return self.raise_or_json(response)

    def get_token_url(self, app_name, expires='1day', write_access=True):
        "Crete URL temporary link for the user to generate token"

        url = f"https://trello.com/1/authorize?key={self._apikey}&"
        url+= f"name={quote(app_name)}&"
        url+= f"expiration={expires}&"
        url+= "response_type=token&"
        url+= f"scope={'read,write' if write_access else 'read'}"
        return url
