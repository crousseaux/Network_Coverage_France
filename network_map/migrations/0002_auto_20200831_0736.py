import pandas as pd
from django.db import migrations


def create_cities(apps, schema_editor):
    cities_df = pd.read_csv('data/cities.csv')
    City = apps.get_model('network_map', 'City')
    new_cities = []
    for index, row in cities_df.iterrows():
        new_city = City(name=row.city)
        new_cities.append(new_city)
    City.objects.bulk_create(new_cities)


def create_providers(apps, schema_editor):
    operators_df = pd.read_csv('data/operators.csv')
    Provider = apps.get_model('network_map', 'Provider')
    new_operators = []
    for index, row in operators_df.iterrows():
        new_operator = Provider(code=row.code, name=row.provider_name)
        new_operators.append(new_operator)
    Provider.objects.bulk_create(new_operators)


def create_networks(apps, schema_editor):
    networks_df = pd.read_csv('data/networks.csv')
    Network = apps.get_model('network_map', 'Network')
    new_networks = []
    for index, row in networks_df.iterrows():
        new_network = Network(name=row.network_name)
        new_networks.append(new_network)
    Network.objects.bulk_create(new_networks)


class Migration(migrations.Migration):
    dependencies = [
        ('network_map', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_cities),
        migrations.RunPython(create_providers),
        migrations.RunPython(create_networks),
    ]
