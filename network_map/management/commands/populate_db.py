import pandas as pd
from django.core.management.base import BaseCommand

from network_map.models import *


class Command(BaseCommand):
    help = 'Populates database with cities, providers, networks and connectors'

    def handle(self, *args, **options):
        create_cities()
        print('Cities created')
        create_providers()
        print('Providers created')
        create_networks()
        print('Networks created')
        create_city_provider_network()
        print('City provider network connectors created')


def create_cities():
    cities_df = pd.read_csv('data/cities.csv')
    new_cities = []
    for index, row in cities_df.iterrows():
        new_city = City(name=row.city)
        new_cities.append(new_city)
    City.objects.bulk_create(new_cities, ignore_conflicts=True)


def create_providers():
    operators_df = pd.read_csv('data/operators.csv')
    new_operators = []
    for index, row in operators_df.iterrows():
        new_operator = Provider(code=row.code, name=row.provider_name)
        new_operators.append(new_operator)
    Provider.objects.bulk_create(new_operators, ignore_conflicts=True)


def create_networks():
    networks_df = pd.read_csv('data/networks.csv')
    new_networks = []
    for index, row in networks_df.iterrows():
        new_network = Network(name=row.network_name)
        new_networks.append(new_network)
    Network.objects.bulk_create(new_networks, ignore_conflicts=True)


def create_city_provider_network():
    connector_df = pd.read_csv('data/city_provider_network.csv')

    if not connector_df.empty:
        new_connectors = []
        # Fetching now so we don't fetch it later
        network_2g = Network.objects.get(name='2G')
        network_3g = Network.objects.get(name='3G')
        network_4g = Network.objects.get(name='4G')
        # This will be used to keep track of providers already queried so we don't query them several times
        code_to_provider = {}
        for index, row in connector_df.iterrows():
            operator_in_row = row.Operateur
            current_provider = code_to_provider[operator_in_row] if operator_in_row in code_to_provider else Provider.objects.get(code=row.Operateur)
            if operator_in_row in code_to_provider:
                code_to_provider[operator_in_row] = Provider
            current_city = City.objects.get(name=row.city)
            if row['2G']:
                new_connector = NetworkProviderCityConnector(city=current_city,
                                                             network=network_2g,
                                                             provider=current_provider)
                new_connectors.append(new_connector)
            if row['3G']:
                new_connector = NetworkProviderCityConnector(city=current_city,
                                                             network=network_3g,
                                                             provider=current_provider)
                new_connectors.append(new_connector)
            if row['4G']:
                new_connector = NetworkProviderCityConnector(city=current_city,
                                                             network=network_4g,
                                                             provider=current_provider)
                new_connectors.append(new_connector)
        NetworkProviderCityConnector.objects.bulk_create(new_connectors, ignore_conflicts=True)
