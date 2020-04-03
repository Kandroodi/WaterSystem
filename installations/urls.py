from django.conf.urls import url
from . import views

urlpatterns = [
    url('city/new/', views.CityCreate, name='city-new')
]