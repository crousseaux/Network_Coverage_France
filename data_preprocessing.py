import csv
import io
import os
import time
import warnings

import numpy
import pandas
import pyproj
import requests
from pandarallel import pandarallel

start_time = time.time()

# because transfrom is deprecated
warnings.filterwarnings("ignore", category=DeprecationWarning)

LAMBERT = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
WGS84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

# using parallelization to rduce the amount of time
# before 37 min after 8 min
pandarallel.initialize(progress_bar=True, nb_workers=os.cpu_count())


# todo: move csv to data folder
# todo: remove pycaches from repo
# todo: read me (dependencies, how, what) // requirements
# todo: add methods everywhere - add if__main__
# todo: add todo.md -> gerer code postaux, chunks, read_csv, modifier pyproj (use transformer)

# todo later: cors allow all https://www.techiediaries.com/django-cors/

def convert_lambert93_to_gps_coord(x, y):
    lon, lat = pyproj.transform(LAMBERT, WGS84, x, y)
    return pandas.Series((lon, lat))


def get_city_from_gps_coord(csv_file):
    resp = requests.post('https://api-adresse.data.gouv.fr/reverse/csv/', files={'data': csv_file, 'result_columns': 'result_city'})
    resp.raise_for_status()
    data = resp.text
    buffer = io.StringIO(data)
    address_details = pandas.read_csv(buffer, delimiter=',', header=0)
    return address_details[['lon', 'lat', 'result_city']]


def append_operator_name_to_code(code_list):
    mcc_mnc_code_data_frame = pandas.read_csv('data/mcc_mnc_codes.csv', header=0)
    return code_list.merge(mcc_mnc_code_data_frame, how='inner', left_on='Operateur', right_on='MCC-MNC')


# Read csv using pandas library
# we could add chunksize depending on csv size
original_data_frame = pandas.read_csv('data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv',
                                      header=0,
                                      delimiter=';')

# Get rid of NA on the two geographic coordinates and remove duplicate lines
original_data_frame.dropna(subset=['X', 'Y'], inplace=True)
original_data_frame.drop_duplicates(inplace=True)

# Get list of all networks
networks = original_data_frame.columns[-3:]
with open("data/networks.csv", mode='w') as csv_file:
    file_writer = csv.writer(csv_file)
    file_writer.writerow(['network_name'])
    for value in networks:
        file_writer.writerow([value])

# Get list of all unique operator
operator = original_data_frame[['Operateur']].drop_duplicates()
operator = append_operator_name_to_code(operator)[['Operateur', 'Nom']]
operator = operator.rename(columns={"Operateur": "code", "Nom": "provider_name"})
operator.to_csv('data/operators.csv', index=False)

# Group row by geolocation
coordinate = original_data_frame[['X', 'Y']].drop_duplicates()
# Get GPS coordinates
coordinate[['lon', 'lat']] = coordinate.parallel_apply(lambda current_row: convert_lambert93_to_gps_coord(current_row['X'], current_row['Y']), axis=1)

minutes = int((time.time() - start_time) / 60)
print("--- %s minutes after coordinate conversion---" % minutes)
# Create csv with GPS lat and long coordinates
# 100 lines is about 4kb -> 100,000 lines are 4Mb
# the api allows us 50Mb ~ 1,000,000 lines
# we only have 70,000 lines in our original dataset
# we don't need to chunk
# print('____________Size of csv (kB)____________')
# print(sys.getsizeof(coordinate) / 1000)

city_details = pandas.DataFrame()
for idx, chunk in enumerate(numpy.array_split(coordinate, 10)):
    coordinate_csv = chunk.to_csv(columns=['lat', 'lon'], index=False)
    # Get all cities from GPS coordinate
    current_city_details = get_city_from_gps_coord(coordinate_csv).dropna()
    print('__________Chunk done__________')
    if city_details.empty:
        city_details = current_city_details
    else:
        city_details.append(current_city_details)

# Get unique cities
print('____________Total number of cities____________')
print(len(city_details))
city_details = city_details.rename(columns={"result_city": "city"})
cities = city_details[['city']].drop_duplicates()
print('____________Number of cities____________')
print(len(cities))
cities.to_csv('data/cities.csv', index=False)

# we don't need this type of precision bc we're looking at cities and gives us 100% match
city_details = city_details.round({'lon': 12, 'lat': 12})
coordinate = coordinate.round({'lon': 12, 'lat': 12})
city_details_withXY = city_details.merge(coordinate, on=['lon', 'lat'])

city_network_provider = city_details_withXY.merge(original_data_frame, on=['X', 'Y'])[['city', 'Operateur', '2G', '3G', '4G']]
print('____________Number of network provider cities____________')
city_network_provider.drop_duplicates(inplace=True)
print(len(city_network_provider))
city_network_provider.to_csv('data/city_provider_network.csv', index=False)

# aws cluster spark
# si non technique d'analyse de donnees -> cluster

print("--- %s seconds ---" % (time.time() - start_time))
minutes = int((time.time() - start_time) / 60)
print("--- %s minutes ---" % minutes)
