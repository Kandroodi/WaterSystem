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
    url(r'^textualevidence/new/$', views.TextualEvidenceCreatView.as_view(), name='textualevidence-insert'),
    url(r'^textualevidence/new/(?P<pk>\d+)/$', views.TextualEvidenceUpdateView.as_view(), name='textualevidence-update'),
    url(r'^textualevidence/delete/(?P<pk>\d+)/$', views.TextualEvidenceDeleteView.as_view(), name='textualevidence-delete'),
    path('textualevidence/list', views.TextualEvidenceListView.as_view(), name='textualevidence-list'),
    url(r'^sourcetype/new/$', views.SourceTypeCreatView.as_view(), name='sourcetype-insert'),
    url(r'^sourcetype/new/(?P<pk>\d+)/$', views.SourceTypeUpdateView.as_view(), name='sourcetype-update'),
    url(r'^sourcetype/delete/(?P<pk>\d+)/$', views.SourceTypeDeleteView.as_view(), name='sourcetype-delete'),
    path('sourcetype/list', views.SourceTypeListView.as_view(), name='sourcetype-list'),
    url(r'^materialevidence/new/$', views.MaterialEvidenceCreatView.as_view(), name='materialevidence-insert'),
    url(r'^materialevidence/new/(?P<pk>\d+)/$', views.MaterialEvidenceUpdateView.as_view(), name='materialevidence-update'),
    url(r'^materialevidence/delete/(?P<pk>\d+)/$', views.MaterialEvidenceDeleteView.as_view(), name='materialevidence-delete'),
    path('materialevidence/list', views.MaterialEvidenceListView.as_view(), name='materialevidence-list'),
    url(r'^watersystem/new/$', views.WaterSystemCreatView.as_view(), name='watersystem-insert'),
    url(r'^watersystem/new/(?P<pk>\d+)/$', views.WaterSystemUpdateView.as_view(), name='watersystem-update'),
    url(r'^watersystem/delete/(?P<pk>\d+)/$', views.WaterSystemDeleteView.as_view(), name='watersystem-delete'),
    path('watersystem/list', views.WaterSystemListView.as_view(), name='watersystem-list'),
    url(r'^purpose/new/$', views.PurposeCreatView.as_view(), name='purpose-insert'),
    url(r'^purpose/new/(?P<pk>\d+)/$', views.PurposeUpdateView.as_view(), name='purpose-update'),
    url(r'^purpose/delete/(?P<pk>\d+)/$', views.PurposeDeleteView.as_view(), name='purpose-delete'),
    path('purpose/list', views.PurposeListView.as_view(), name='purpose-list'),
    url(r'^institutiontype/new/$', views.InstitutionTypeCreatView.as_view(), name='institutiontype-insert'),
    url(r'^institutiontype/new/(?P<pk>\d+)/$', views.InstitutionTypeUpdateView.as_view(), name='institutiontype-update'),
    url(r'^institutiontype/delete/(?P<pk>\d+)/$', views.InstitutionTypeDeleteView.as_view(), name='institutiontype-delete'),
    path('institutiontype/list', views.InstitutionTypeListView.as_view(), name='institutiontype-list'),
    url(r'^religion/new/$', views.ReligionCreatView.as_view(), name='religion-insert'),
    url(r'^religion/new/(?P<pk>\d+)/$', views.ReligionUpdateView.as_view(), name='religion-update'),
    url(r'^religion/delete/(?P<pk>\d+)/$', views.ReligionDeleteView.as_view(), name='religion-delete'),
    path('religion/list', views.ReligionListView.as_view(), name='religion-list'),
    # Relations
    # ------------------------------------------------------------------------------------------------------------------
    url(r'^citypersonrelation/new/$', views.CityPersonRelationCreatView.as_view(), name='citypersonrelation-insert'),
    url(r'^citypersonrelation/new/(?P<pk>\d+)/$', views.CityPersonRelationUpdateView.as_view(), name='citypersonrelation-update'),
    url(r'^citypersonrelation/delete/(?P<pk>\d+)/$', views.CityPersonRelationDeleteView.as_view(), name='citypersonrelation-delete'),
    path('citypersonrelation/list', views.CityPersonRelationListView.as_view(), name='citypersonrelation-list'),
    url(r'^personinstitutionrelation/new/$', views.PersonInstitutionRelationCreatView.as_view(), name='personinstitutionrelation-insert'),
    url(r'^personinstitutionrelation/new/(?P<pk>\d+)/$', views.PersonInstitutionRelationUpdateView.as_view(), name='personinstitutionrelation-update'),
    url(r'^personinstitutionrelation/delete/(?P<pk>\d+)/$', views.PersonInstitutionRelationDeleteView.as_view(), name='personinstitutionrelation-delete'),
    path('personinstitutionrelation/list', views.PersonInstitutionRelationListView.as_view(), name='personinstitutionrelation-list'),
    url(r'^personinstallationrelation/new/$', views.PersonInstallationRelationCreatView.as_view(), name='personinstallationrelation-insert'),
    url(r'^personinstallationrelation/new/(?P<pk>\d+)/$', views.PersonInstallationRelationUpdateView.as_view(), name='personinstallationrelation-update'),
    url(r'^personinstallationrelation/delete/(?P<pk>\d+)/$', views.PersonInstallationRelationDeleteView.as_view(), name='personinstallationrelation-delete'),
    path('personinstallationrelation/list', views.PersonInstallationRelationListView.as_view(), name='personinstallationrelation-list'),
    url(r'^cityinstallationrelation/new/$', views.CityInstallationRelationCreatView.as_view(), name='cityinstallationrelation-insert'),
    url(r'^cityinstallationrelation/new/(?P<pk>\d+)/$', views.CityInstallationRelationUpdateView.as_view(), name='cityinstallationrelation-update'),
    url(r'^cityinstallationrelation/delete/(?P<pk>\d+)/$', views.CityInstallationRelationDeleteView.as_view(), name='cityinstallationrelation-delete'),
    path('cityinstallationrelation/list', views.CityInstallationRelationListView.as_view(), name='cityinstallationrelation-list'),
]