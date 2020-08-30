from django.db import migrations


def create_city_network_providers(apps, schema_editor):
    return


class Migration(migrations.Migration):
    dependencies = [
        ('network_map', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_city_network_providers),
    ]
