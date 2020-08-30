import warnings

import pandas
import pyproj
import requests

warnings.filterwarnings("ignore", category=DeprecationWarning)
counter = 0

lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')


def convert_lambert93_to_gps_coord(x, y):
    lon, lat = pyproj.transform(lambert, wgs84, x, y)
    global counter
    counter += 1
    print(counter)
    return pandas.Series((lon, lat))


def get_city_from_gps_coord(lon, lat):
    resp = requests.get('https://api-adresse.data.gouv.fr/reverse/?lon=' + str(lon) + '&lat=' + str(lat))
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('GET /tasks/ {}'.format(resp.status_code))
    resp = resp.json()
    address_details = resp['features'][0]['properties'] if resp['features'] and len(resp['features']) > 0 and resp['features'][0] and resp['features'][0]['properties'] else None
    return address_details['city'] if address_details is not None else ''


reader = pandas.read_csv('2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv',
                         header=0,
                         delimiter=';', skiprows=[i for i in range(10, 77000)])

reader.dropna(subset=['X', 'Y'], inplace=True)

reader.drop_duplicates(inplace=True)

# for index, row in reader.iterrows():
#     break

operator = reader.Operateur.unique()

coordinate = reader.groupby(['X', 'Y']).size().reset_index()

coordinate[['lon', 'lat']] = coordinate.apply(lambda current_row: convert_lambert93_to_gps_coord(current_row['X'], current_row['Y']), axis=1)

coordinate['city'] = coordinate.apply(lambda current_row: get_city_from_gps_coord(current_row['lon'], current_row['lat']), axis=1)
print(coordinate)

cities = coordinate.city.unique()
print(cities)
