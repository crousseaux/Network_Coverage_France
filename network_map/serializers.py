from rest_framework import serializers

from . import models


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Provider


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Network


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.City


class NetworkProviderCityConnectorSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField(source='city.name', read_only=True)
    provider = serializers.StringRelatedField(source='provider.name', read_only=True)
    network = serializers.StringRelatedField(source='network.name', read_only=True)

    class Meta:
        fields = ('city', 'provider', 'network')
        model = models.NetworkProviderCityConnector
