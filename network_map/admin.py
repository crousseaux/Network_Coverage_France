from django.contrib import admin

from .models import *

# Register models for the admin console
admin.site.register(Provider)
admin.site.register(City)
admin.site.register(Network)
admin.site.register(NetworkProviderCityConnector)
