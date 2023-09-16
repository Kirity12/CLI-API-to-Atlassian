import json
from requests.utils import quote
import requests


API_KEY = "26dea0c6d8f4574827f3e06654ab5102"
TOKEN_KEY = "ATTA0c9670fe99c679e661aeef28cd9275b160270a70dff5e00fc4cd516fe1f321ef059D598F"

class TrelloApi(object):
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
        status = resp.status_code
        if status==200:
            obj = json.loads(resp.text)
        else:
            obj = None
        return status, obj

    def set_token(self, token):
        self._token = token
        self._query['token'] = token

    def add_card(self, name, col_id, desc=None, idLabels=[]):
        
        url = self.url + "cards"
        query = {
                'key': self._apikey,
                'token': self._token,
                'name': name,
                'desc': desc,
                'idList': col_id,
                'idLabels': idLabels if idLabels else None
                }
        
        response = requests.request(
                                    "POST",
                                    url,
                                    params=query,
                                    headers=self.headers,
                                    )

        return self.raise_or_json(response)
    
    def add_label_to_card(self, card_id, idLabels):
        
        url = self.url + f"cards/{card_id}/idLabels"
        
        response = requests.request(
                                    "POST",
                                    url,
                                    params=self._query,
                                    headers=self.headers,
                                    data={'value': idLabels}
                                    )

        return self.raise_or_json(response)
    
    def create_label(self,name, color, idBoard):

        url = "https://trello.com/1/labels"

        response = requests.request(
                                    "POST",
                                    url,
                                    params=self._query,
                                    data={"name": name, "color": color, "idBoard": idBoard})
        
        return self.raise_or_json(response)
    
    def get_boards(self):
        url = self.url + "/members/me/boards"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self._query,
                                    headers=self.headers
                                    )

        return self.raise_or_json(response)
    
    def get_columns(self, board_id):
        url = self.url + f"boards/{board_id}/lists"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self._query,
                                    headers=self.headers
                                    )

        return self.raise_or_json(response)
    
    def get_labels(self, board_id):

        url = self.url + f"boards/{board_id}/labels"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self._query,
                                    headers=self.headers
                                    )

        return self.raise_or_json(response)
    
    def get_cards(self, board_id):

        url = self.url + f"boards/{board_id}/cards"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self._query,
                                    headers=self.headers
                                    )

        return self.raise_or_json(response)
    
    def get_token_url(self, app_name, expires='30days', write_access=True):
        url = f"https://trello.com/1/authorize?key={API_KEY}&"
        url+= f"name={quote(app_name)}&"
        url+= f"expiration={expires}&"
        url+= f"response_type=token&"
        url+= f"scope={'read,write' if write_access else 'read'}"
        return url


if __name__ == "__main__":

    board_id = "6503765a9dfc3faf1dc65d24"
    col_id = "6503765a250478954fb2c0f2"
    card_id = "6503765bfb7d456f54dc96ae"
    label_id = ["6503765a59075ce50db4ac43", "6503765a59075ce50db4ac47"]

    app = TrelloApi(API_KEY,TOKEN_KEY)

    st, obj = app.get_boards()
    print(st)
    st, obj = app.get_columns(board_id)
    print(st)
    st, obj = app.get_labels(board_id)
    print(st, obj[1])
    st, obj = app.get_cards(board_id)
    print(st)
    st = app.get_token_url('NG')
    print(st)
    st, obj = app.add_card('TEST', col_id, 'test', label_id)
    print(st)
    st, obj = app.add_label_to_card(card_id, label_id[1])
    print(st)
    st, obj = app.create_label('New', 'red', board_id)
    print(st)