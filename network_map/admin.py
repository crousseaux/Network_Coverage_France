from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Provider)
admin.site.register(City)
admin.site.register(Network)
admin.site.register(NetworkProviderCityConnector)
