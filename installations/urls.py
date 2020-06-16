from django.conf.urls import url
from django.urls import path
from . import views

# TEMPLATE URLS
app_name = 'installations'

urlpatterns = [
    path('register/', views.register , name='register'), # Sign up
    path('logout/', views.user_logout, name='logout'), # Logout
    path('login/', views.user_login, name='user_login'), # Login
    path('', views.Home, name='home'), # get and post req. for insert operation
    path('city/new/', views.CityCreate, name='city-insert'), # get and post req. for insert operation
    path('city/new/<int:id>/', views.CityCreate, name='city-update'), # get and post req. for update operation
    path('city/delete/<int:id>/', views.CityDelete, name='city-delete'),
    path('city/list/', views.CityList, name='city-list'),  # get request to retrieve and display all records
    path('institution/new/', views.InstitutionCreate, name='institution-insert'),  # get and post req. for insert operation
    path('institution/new/<int:id>/', views.InstitutionCreate, name='institution-update'),  # get and post req. for update operation
    path('institution/delete/<int:id>/', views.InstitutionDelete, name='institution-delete'),
    path('institution/list/', views.InstitutionList, name='institution-list'),  # get request to retrieve and display all records
    path('person/new/', views.PersonCreate, name='person-insert'),
    path('person/new/<int:id>/', views.PersonCreate, name='person-update'),
    path('person/delete/<int:id>/', views.PersonDelete, name='person-delete'),
    path('person/list/', views.PersonList, name='person-list'),
    path('bibliography/new/', views.BibliographyCreate, name='bibliography-insert'),
    path('bibliography/new/<int:id>/', views.BibliographyCreate, name='bibliography-update'),
    path('bibliography/delete/<int:id>/', views.BibliographyDelete, name='bibliography-delete'),
    path('bibliography/list/', views.BibliographyList, name='bibliography-list'),
    path('installation/new/', views.InstallationCreate, name='installation-insert'),
    path('installation/new/<int:id>/', views.InstallationCreate, name='installation-update'),
    path('installation/delete/<int:id>/', views.InstallationDelete, name='installation-delete'),
    path('installation/list/', views.InstallationList, name='installation-list'),
]