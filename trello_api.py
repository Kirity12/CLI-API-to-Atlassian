import json
from requests.utils import quote
import requests


API_KEY = "26dea0c6d8f4574827f3e06654ab5102"
TOKEN_KEY = "ATTA0c9670fe99c679e661aeef28cd9275b160270a70dff5e00fc4cd516fe1f321ef059D598F"
SECRET_KEY = "aa7a7b4c1cd435eb43df7175608ebd531b9295ef79a0428f484959584f67d980"

class TrelloApi(object):
    def __init__(self, apikey, token=None):
        self._apikey = API_KEY
        self._token = TOKEN_KEY
        self.headers = {
                        "Accept": "application/json"
                       }
        self.url = "https://api.trello.com/1/"

    def raise_or_json(self, resp):
        return json.dumps(json.loads(resp.text), indent=4, separators=(",", ": "))

    def set_token(self, token):
        self._token = token
        self.cards._token = token

    def new_card(self, name, idList, desc=None, pos=None, due=None, start=None, dueComplete=None, idMembers=None, idLabels=None, urlSource=None, fileSource=None, idCardSource=None, keepFromSource=None):
        
        url = self.url + "cards"
        query = {
                'key': API_KEY,
                'token': TOKEN_KEY,
                'name': name,
                'desc': desc,
                'idList': idList
                }
        
        response = requests.request(
                                    "POST",
                                    url,
                                    params=query,
                                    headers=headers
                                    )

        return self.raise_or_json(response)
        
    
    def get_boards(self):
        url = self.url + "boards"
        query = {
                'key': self._apikey,
                'token': self._token
                }
        response = requests.request(
                                    "GET",
                                    url,
                                    params=query,
                                    headers=headers
                                    )

        return self.raise_or_json(response)
    
    def get_columns(self, board_id):

        url = self.url + f"boards/{board_id}/lists"
        query = {
                'key': self._apikey,
                'token': self._token,
                'id': board_id
                }
        response = requests.request(
                                    "GET",
                                    url,
                                    params=query,
                                    headers=headers
                                    )

        return self.raise_or_json(response)
    
    def get_token_url(self, app_name, expires='30days', write_access=True):
        return f'''https://trello.com/1/authorize?key={self._apikey}& 
                                                name={quote(app_name)}&
                                                expiration={expires}&
                                                response_type=token&
                                                scope={'read,write' if write_access else 'read'}'''
    
    def set_token(self, token):
        self._token = token


# url = "https://api.trello.com/1/boards/6503765a9dfc3faf1dc65d24/lists"
# url = "https://api.trello.com/1/members/me/boards"

def get_token_url( app_name, expires='30days', write_access=True):
        url = f"https://trello.com/1/authorize?key={API_KEY}&"
        url+= f"name={quote(app_name)}&"
        url+= f"expiration={expires}&"
        url+= f"response_type=token&"
        url+= f"scope={'read,write' if write_access else 'read'}"
        return url

print(get_token_url('NG'))

url = "https://api.trello.com/1/cards"

headers = {
  "Accept": "application/json"
}

query = {
#   'id': '6503765a9dfc3faf1dc65d24',
  'key': API_KEY,
  'token': TOKEN_KEY,
  'name': "Test Card",
  'desc': "Doing",
  'idList': "6503765a250478954fb2c0f2"
}

# response = requests.post(url, json=query)
# print(json.loads(response.text))

response = requests.request(
   "POST",
   url,
   headers=headers,
   params=query
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
