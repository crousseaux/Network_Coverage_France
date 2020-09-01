import requests


def get_city_from_address(address):
    resp = requests.get('https://api-adresse.data.gouv.fr/search/', params={'q': address})
    resp.raise_for_status()
    resp = resp.json()
    return resp["features"][0]["properties"]["city"]