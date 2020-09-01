from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .services import geocoding_service


class ProviderList(generics.ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ProviderDetail(generics.RetrieveAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityDetail(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class NetworkList(generics.ListAPIView):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class NetworkDetail(generics.RetrieveAPIView):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class ConnectorList(generics.ListAPIView):
    queryset = NetworkProviderCityConnector.objects.all()
    serializer_class = NetworkProviderCityConnectorSerializer


class ConnectorDetail(generics.RetrieveAPIView):
    queryset = NetworkProviderCityConnector.objects.all()
    serializer_class = NetworkProviderCityConnectorSerializer


class NetworkMapping(APIView):
    def get(self, request):
        address = request.query_params.get('q', None)
        city = geocoding_service.get_city_from_address(address)
        networks = Network.objects.all()
        connectors = NetworkProviderCityConnector.objects.filter(city__name=city)
        payload = {}
        for connector in connectors:
            provider_name = connector.provider.name
            if provider_name not in payload:
                network_payload = {network.name: False for network in networks}
                payload[provider_name] = network_payload
            current_provider = payload[provider_name]
            current_provider[connector.network.name] = True
        return Response(payload)
