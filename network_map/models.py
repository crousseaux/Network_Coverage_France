from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Provider(BaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Network(BaseModel):
    name = models.CharField(max_length=50)


class City(BaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class NetworkProviderCityConnector(BaseModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
