import requests

api_base = "https://graph.microsoft.com/v1.0/"


def get_user_data(token):
    headers = {"Authorization": "Bearer " + token}
    r = requests.get(api_base + "me", headers=headers)
    r.raise_for_status()
    data = r.json()
    return {
        "id": data["id"],
        "name": data["displayName"],
        "email": data["userPrincipalName"],
        "givenName": data["givenName"],
        "surname": data["surname"],
    }
