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
    class Meta:
        fields = '__all__'
        model = models.NetworkProviderCityConnector
