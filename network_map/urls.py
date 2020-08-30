from django.urls import path

from . import views

urlpatterns = [
    path('provider/', views.ProviderList.as_view()),
    path('provider/<int:pk>/', views.ProviderDetail.as_view()),
    path('city/', views.CityList.as_view()),
    path('city/<int:pk>/', views.CityDetail.as_view()),
]
