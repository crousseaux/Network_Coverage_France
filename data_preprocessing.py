import csv
import io
import os
import warnings

import numpy
import pandas
import pyproj
import requests
from pandarallel import pandarallel

# hide deprecation warnings from console as pyproj transform is deprecated
warnings.filterwarnings("ignore", category=DeprecationWarning)

# constants used to convert lambert 93 coordinates into longitude, latitude
LAMBERT = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
WGS84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

# using parallelization to reduce the amount of time it takes to convert lambert 93 to gps coordinates
# Performances: - Before: 37 min | After: 8 min with 8 cpus
pandarallel.initialize(progress_bar=True, nb_workers=os.cpu_count())


def main():
    original_data_frame = get_original_data_frame()
    create_networks_csv(original_data_frame)
    create_operators_csv(original_data_frame)
    gps_coordinates = get_gps_coordinates(original_data_frame)
    city_details_df = get_city_details(gps_coordinates)
    create_cities_csv(city_details_df)
    create_city_provider_network(original_data_frame, city_details_df, gps_coordinates)


def get_original_data_frame():
    # Read csv using pandas library
    # we could add chunksize depending on csv size
    original_data_frame = pandas.read_csv('data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv',
                                          header=0,
                                          delimiter=';')
    # Get rid of NA on the two lambert 93 coordinates and remove duplicate lines
    original_data_frame.dropna(subset=['X', 'Y'], inplace=True)
    original_data_frame.drop_duplicates(inplace=True)
    return original_data_frame


def create_networks_csv(original_data_frame):
    # Get list of all networks
    # We know that the last 3 column names of the original data source are the 3 network coverage
    networks = original_data_frame.columns[-3:]
    with open("data/networks.csv", mode='w') as csv_file:
        file_writer = csv.writer(csv_file)
        file_writer.writerow(['network_name'])
        for value in networks:
            file_writer.writerow([value])


def create_operators_csv(original_data_frame):
    # Get list of all unique operators
    operators = original_data_frame[['Operateur']].drop_duplicates()
    # Get operator names from code
    operators = append_operator_details_from_code(operators)[['Operateur', 'Nom']]
    operators = operators.rename(columns={"Operateur": "code", "Nom": "provider_name"})
    operators.to_csv('data/operators.csv', index=False)


def get_gps_coordinates(original_data_frame):
    # Group row by geolocation
    coordinates = original_data_frame[['X', 'Y']].drop_duplicates()
    # Get GPS coordinates
    # Use parallelization
    coordinates[['lon', 'lat']] = coordinates.parallel_apply(lambda current_row: convert_lambert93_to_gps_coord(current_row['X'], current_row['Y']), axis=1)
    return coordinates


def get_city_details(coordinates):
    # Creates a dataframe with longitude, latitude, city
    # geo.api.gouv can only receive files up to 6 Mb
    # 100 lines is about 4kb -> 100,000 lines are 4Mb
    # the api allows us 6Mb ~ 150,000 lines
    # we only have 70,000 lines in our original dataset
    # we should not need to chunk
    city_details = pandas.DataFrame()
    for idx, chunk in enumerate(numpy.array_split(coordinates, 10)):
        coordinate_csv = chunk.to_csv(columns=['lat', 'lon'], index=False)
        # Get all cities from GPS coordinate
        current_city_details = get_city_from_gps_coord(coordinate_csv).dropna()
        if city_details.empty:
            city_details = current_city_details
        else:
            city_details = city_details.append(current_city_details)
    return city_details


def create_cities_csv(city_details):
    # Get unique cities
    city_details = city_details.rename(columns={"result_city": "city"})
    cities = city_details[['city']].drop_duplicates()
    cities.to_csv('data/cities.csv', index=False)


def create_city_provider_network(original_data_frame, city_details_df, gps_coordinates):
    # match city to X,Y
    # reducing a little bit of precision to match geo.api.gouv precision
    # this doesn't impact us because we are looking at city level precision
    city_details = city_details_df.round({'lon': 12, 'lat': 12})
    gps_coordinates = gps_coordinates.round({'lon': 12, 'lat': 12})
    city_details_with_xy = city_details.merge(gps_coordinates, on=['lon', 'lat'])

    # match city name to original network coverage and provider dataset using columns X and Y
    city_network_provider = city_details_with_xy.merge(original_data_frame, on=['X', 'Y'])[['city', 'Operateur', '2G', '3G', '4G']]
    city_network_provider.drop_duplicates(inplace=True)
    city_network_provider.to_csv('data/city_provider_network.csv', index=False)


def convert_lambert93_to_gps_coord(x, y):
    lon, lat = pyproj.transform(LAMBERT, WGS84, x, y)
    return pandas.Series((lon, lat))


# Reverse search: retrieve an address from gps coordinates
def get_city_from_gps_coord(csv_file):
    resp = requests.post('https://api-adresse.data.gouv.fr/reverse/csv/', files={'data': csv_file, 'result_columns': 'result_city'})
    resp.raise_for_status()
    data = resp.text
    buffer = io.StringIO(data)
    address_details = pandas.read_csv(buffer, delimiter=',', header=0)
    return address_details[['lon', 'lat', 'result_city']]


# Get the operator name using mcc and mnc codes from the data source
def append_operator_details_from_code(code_list):
    mcc_mnc_code_data_frame = pandas.read_csv('data/mcc_mnc_codes.csv', header=0)
    return code_list.merge(mcc_mnc_code_data_frame, how='inner', left_on='Operateur', right_on='MCC-MNC')


if __name__ == "__main__":
    main()
