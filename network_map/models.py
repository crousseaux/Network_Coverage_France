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
    name = models.CharField(max_length=20, unique=True)


class City(BaseModel):
    name = models.CharField(max_length=50, unique=True)


class NetworkProviderCityConnector(BaseModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, unique=False)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, unique=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, unique=False)

    class Meta:
        unique_together = ('city', 'network', 'provider')
