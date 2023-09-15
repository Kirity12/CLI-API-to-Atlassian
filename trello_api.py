import json
from requests.utils import quote
import requests


API_KEY = "26dea0c6d8f4574827f3e06654ab5102"
TOKEN_KEY = "ATTA0c9670fe99c679e661aeef28cd9275b160270a70dff5e00fc4cd516fe1f321ef059D598F"
SECRET_KEY = "aa7a7b4c1cd435eb43df7175608ebd531b9295ef79a0428f484959584f67d980"

class TrelloApi(object):
    def __init__(self, apikey, token=None):
        self._apikey = apikey
        self._token = token
        self.headers = {
                        "Accept": "application/json"
                       }
        self.query = {
                'key': self._apikey,
                'token': self._token,
                }
        self.url = "https://api.trello.com/1/"

    def raise_or_json(self, resp):
        status = resp.status_code
        if status==200:
            obj = json.dumps(json.loads(resp.text), indent=4, separators=(",", ": "))
        else:
            obj = None
        return status, obj

    def set_token(self, token):
        self._token = token
        self.cards._token = token

    def add_card(self, name, boardId, desc=None, idLabels=None):
        
        url = self.url + "cards"
        query = {
                'key': self._apikey,
                'token': self._token,
                'name': name,
                'desc': desc,
                'idList': boardId,
                'idLabels': ['6503765a59075ce50db4ac43','6503765a59075ce50db4ac47']
                }
        
        response = requests.request(
                                    "POST",
                                    url,
                                    params=query,
                                    headers=self.headers,
                                    )

        return self.raise_or_json(response)
    
    def get_boards(self):
        url = self.url + "/members/me/boards"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self.query,
                                    headers=self.headers
                                    )

        return self.raise_or_json(response)
    
    def get_columns(self, board_id):
        url = self.url + f"boards/{board_id}/lists"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self.query,
                                    headers=self.headers
                                    )

        return self.raise_or_json(response)
    
    def get_labels(self, board_id):

        url = self.url + f"boards/{board_id}/labels"

        response = requests.request(
                                    "GET",
                                    url,
                                    params=self.query,
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
    
    def set_token(self, token):
        self._token = token

board_id = "6503765a9dfc3faf1dc65d24"
col_id = "6503765a250478954fb2c0f2"

app = TrelloApi(API_KEY,TOKEN_KEY)

st, _ = app.get_boards()
print(st)
st, _ = app.get_columns(board_id)
print(st)
st, obj = app.get_labels(board_id)
print(st)
st = app.get_token_url('NG')
print(st)
st, _ = app.add_card('TEST', col_id, 'test')
print(st)
