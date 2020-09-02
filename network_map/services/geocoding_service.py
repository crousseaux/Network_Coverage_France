import requests


# helper function to retrieve a city from a given address using geo.api.gouv api
def get_city_from_address(address):
    resp = requests.get('https://api-adresse.data.gouv.fr/search/', params={'q': address})
    resp.raise_for_status()
    resp = resp.json()
    # todo: handle errors
    return resp["features"][0]["properties"]["city"]
