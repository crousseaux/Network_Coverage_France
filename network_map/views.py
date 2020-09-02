from requests.exceptions import HTTPError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .services import geocoding_service


# Provider views
class ProviderList(generics.ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ProviderDetail(generics.RetrieveAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


# City views
class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityDetail(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


# Network views
class NetworkList(generics.ListAPIView):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class NetworkDetail(generics.RetrieveAPIView):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


# City provider network views
class ConnectorList(generics.ListAPIView):
    queryset = NetworkProviderCityConnector.objects.all()
    serializer_class = NetworkProviderCityConnectorSerializer


class ConnectorDetail(generics.RetrieveAPIView):
    queryset = NetworkProviderCityConnector.objects.all()
    serializer_class = NetworkProviderCityConnectorSerializer


# network mapping main view
class NetworkMapping(APIView):
    def get(self, request):
        # Get address from the query parameter
        address = request.query_params.get('q', None)
        if not address:
            return Response({'error': 'Address is missing. Make sure to provide an address'}, status=status.HTTP_400_BAD_REQUEST)
        # Find the city of the address using geo.api.gouv api
        try:
            city = geocoding_service.get_city_from_address(address)
        except HTTPError:
            return Response({'error': 'Unable to get connect to data.gouv.fr API. Please try again.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if city is None:
            return Response({'error': 'Address not recognized. Make sure it is correct.'}, status=status.HTTP_400_BAD_REQUEST)
        # querying all networks as they will all be part of the payload
        networks = Network.objects.all()
        # get all the network providers and coverage of the requested city
        connectors = NetworkProviderCityConnector.objects.filter(city__name=city)
        payload = {}
        for connector in connectors:
            provider_name = connector.provider.name
            if provider_name not in payload:
                # initialise payload by setting all networks to false for the current provider if not done already
                network_payload = {network.name: False for network in networks}
                payload[provider_name] = network_payload
            # set the current network coverage to true
            current_provider = payload[provider_name]
            current_provider[connector.network.name] = True
        return Response(payload)
