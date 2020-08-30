from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProviderList.as_view()),
    path('<int:pk>/', views.ProviderDetail.as_view()),
]
