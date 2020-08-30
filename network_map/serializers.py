from rest_framework import serializers

from . import models


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'created_at', 'updated_at']
        model = models.Provider


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'created_at', 'updated_at']
        model = models.Network


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'created_at', 'updated_at']
        model = models.City


class NetworkProviderCityConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['city', 'network', 'provider', 'created_at', 'updated_at']
        model = models.NetworkProviderCityConnector
