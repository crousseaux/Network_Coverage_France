from django.urls import path

from . import views

urlpatterns = [
    path('provider/', views.ProviderList.as_view()),
    path('provider/<int:pk>/', views.ProviderDetail.as_view()),
    path('city/', views.CityList.as_view()),
    path('city/<int:pk>/', views.CityDetail.as_view()),
    path('network/', views.NetworkList.as_view()),
    path('network/<int:pk>/', views.NetworkDetail.as_view()),
    path('connector/', views.ConnectorList.as_view()),
    path('connector/<int:pk>/', views.ConnectorDetail.as_view()),
    path('', views.NetworkMapping.as_view()),
]
