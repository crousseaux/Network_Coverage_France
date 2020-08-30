from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Provider(BaseModel):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)


class Network(BaseModel):
    name = models.CharField(unique=True, max_length=20)


class City(BaseModel):
    name = models.CharField(max_length=50, unique=True)


class NetworkProviderCityConnector(BaseModel):
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    network_id = models.ForeignKey(Network, on_delete=models.CASCADE)
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('city_id', 'network_id', 'provider_id')
