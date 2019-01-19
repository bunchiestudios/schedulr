import requests

api_base = 'https://www.googleapis.com/oauth2/v1'

def get_user_data(token):
    headers = {
        'Authorization' : 'Bearer ' + token
    }
    r = requests.get(api_base + '/userinfo?alt=json', headers=headers)
    r.raise_for_status()
    data = r.json()
    return {
        'id': data['id'],
        'name': data['name'],
        'email': data['email'],
        'givenName': data['given_name'],
        'surname': data['family_name']
    }