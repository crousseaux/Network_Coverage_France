from rest_framework import generics

from .models import *
from .serializers import *


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
