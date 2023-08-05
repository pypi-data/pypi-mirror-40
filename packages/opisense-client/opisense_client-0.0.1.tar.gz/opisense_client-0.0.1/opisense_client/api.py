import requests
from urllib.parse import urlencode
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import json

#get api credentials
with open("./Files/api_credentials.JSON", encoding="utf-8") as file:
    api_credentials = json.load(file)

# ==== Push Opisense Data ====
#TODO : refactor this function with json.dumps() function
def push_opisense_data(data: dict, opisense_token: str):
    data = data[['date', 'variableId', 'value']]
    jsonObject = '{data:' + data.to_json(orient='records', date_format='iso') + '}'
    response = requests.post('https://push.opinum.com/api/standard/', data=jsonObject,
                             headers={"Authorization": opisense_token, "Content-Type": "application/json"})
    print(response.status_code)
    return response


# ==== Get Opisense Object ====
def get_opisense_object(token: str, object_type: str, query: dict):
    """ Get every Opisense object corresponding to the query filter"""
    url = "https://api.opinum.com:443/" + object_type + "?" + urlencode(query, True)
    headers = {"Accept": "application/json",
               "Authorization": token,
               "X-Opisense-Api-Version": "1.1"}
    result = requests.get(url, headers=headers).text
    result = json.loads(str(result), encoding='utf-8')
    return result


# ==== Get Opisense Token ====
def get_opisense_token(usr: str, pwd: str):
    client_id = api_credentials['client_id']
    client_secret = api_credentials['client_secret']
    scope = ["opisense-api push-data profile openid opisense-dataset"]
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
    token = oauth.fetch_token(token_url='https://identity.opinum.com/connect/token',
                              scope=scope,
                              username=usr,
                              password=pwd,
                              client_id=client_id,
                              client_secret=client_secret,
                              auth=False)
    account = get_opisense_object("Bearer " + token["access_token"], 'account', {})
    print('You are connected to the account ' + str(account['id']) + ' - ' + str(account['name']))
    return "Bearer " + token["access_token"]


# ==== Delete Opisense Object ====
def delete_opisense_object(token: str, object_type: str, object_id: int):
    url = "https://api.opinum.com/" + object_type + "/" + str(object_id)
    headers = {"Accept": "application/json",
               "Authorization": token,
               "X-Opisense-Api-Version": "1.0"}
    result = requests.delete(url, headers=headers).content
    return result


# ==== Push Opisense Object ====
def push_opisense_object(token: str, object_type: str, opisense_object, object_id=None, source_id=None):
    """ Push object to Opisense
    Manage different methods for variables
    POST method if new object (no id provided)
    PUT method is existing object (id provided) to update"""
    url = "https://api.opinum.com:443/"
    jsonObject = json.dumps(opisense_object)
    headers = {"Content-Type": "application/json",
               "Authorization": token,
               "X-Opisense-Api-Version": "1.1"}
    if object_type == 'variables':
        if object_id == None:
            result = requests.post(url + "variables/source/" + str(source_id), headers=headers, data=jsonObject)
            return json.loads(result.text)
        else:
            result = requests.put(url + "sources/" + str(source_id) + "/variables/" + str(object_id), headers=headers, data=jsonObject)
            if result.status_code == 204:
                return {'id':object_id}
            else:
                return result
    else:
        if object_id == None:
            result = requests.post(url + object_type, headers=headers, data=jsonObject)
            return json.loads(result.text)
        else:
            result = requests.put(url + object_type + "/" + str(object_id), headers=headers, data=jsonObject)
            if result.status_code == 204:
                return {'id':object_id}
            else:
                return result

# === Trigger Dataset ===
def trigger_dataset(token: str, dataset):
    """ WARNING : this function only works on Opisense Local network """
    url = "http://backend.opinum.com:12017/dataset/enqueue"
    body = json.dumps(dataset)
    headers = {"Content-Type": "application/json",
               "Authorization": token,
               # "X-Opisense-Api-Version": "1.1"
                }
    result = requests.post(url , headers=headers, data=body)
    return result

# === Change Opisense Account for current user ===
def change_opisense_account(token:str,accountId:int, usr : str, pwd : str ):
    """ WARNING : Must have Admin rights to work
    Change the admin user account to the one passed to this function
    gets token for the new account"""
    # get user Id
    user = get_opisense_object(token,'/user/info',{})
    user_id = user['id']
    # get user claims
    claims = get_opisense_object(token,'/user/claim/'+user_id,{})
    # get the account claim id
    for claim in claims:
        if claim['claimType'] == 'http://opisense.opinum.com/account':
            claim_id = claim['id']
    # update the claim
    new_claim = {
        'id' : claim_id,
        'userId' : user_id,
        'claimType' : 'http://opisense.opinum.com/account',
        'claimValue' : accountId
    }
    push_opisense_object(token,'/user/claims/edit',new_claim)
    # get token for the new account
    new_token = get_opisense_token(usr, pwd)
    return new_token