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
    path('city/new/<str:view>/', views.CityCreate, name='city-insert'),
    path('city/new/<int:id>', views.CityCreate, name='city-update'), # get and post req. for update operation
    path('city/delete/<int:id>/', views.CityDelete, name='city-delete'),
    path('city/list/', views.CityList, name='city-list'),  # get request to retrieve and display all records
    # path('institution/new/', views.InstitutionCreate, name='institution-insert'),  # get and post req. for insert operation
    path('institution/new/', views.edit_institution, name='institution-insert'),
    path('institution/new/<str:view>/', views.edit_institution, name='institution-insert'),
    path('institution/new/<int:pk>', views.edit_institution, name='institution-update'),
    path('institution/new/<int:pk>/<str:focus>', views.edit_institution, name='institution-update'),
    path('institution/delete/<int:id>/', views.InstitutionDelete, name='institution-delete'),
    path('institution/list/', views.InstitutionList, name='institution-list'),  # get request to retrieve and display all records
    path('institution/<int:pk>', views.InstitutionDetailView.as_view(), name='institution-detail'),
    path('person/new/', views.edit_person, name='person-insert'),
    path('person/new/<str:view>/', views.edit_person, name='person-insert'),
    path('person/new/<int:pk>', views.edit_person, name='person-update'),
    path('person/new/<int:pk>/<str:focus>', views.edit_person, name='person-update'),
    path('person/delete/<int:id>/', views.PersonDelete, name='person-delete'),
    path('person/list/', views.PersonList, name='person-list'),
    path('person/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),
    path('secondaryliterature/new/', views.SecondaryLiteratureCreatView.as_view(), name='secondaryliterature-insert'),
    path('secondaryliterature/new/<str:view>/', views.SecondaryLiteratureCreatView.as_view(), name='secondaryliterature-insert'),
    path('secondaryliterature/new/<int:pk>', views.SecondaryLiteratureUpdateView.as_view(), name='secondaryliterature-update'),
    url(r'^secondaryliterature/delete/(?P<pk>\d+)/$', views.SecondaryLiteratureDeleteView.as_view(), name='secondaryliterature-delete'),
    path('secondaryliterature/list/', views.SecondaryLiteratureListView.as_view(), name='secondaryliterature-list'),
    path('secondaryliterature/<int:pk>', views.SecondaryLiteratureDetailView.as_view(), name='secondaryliterature-detail'),
    # path('installation/new/', views.InstallationCreate, name='installation-insert'),
    path('installation/new/', views.edit_installation, name='installation-insert'),
    path('installation/new/<str:view>/', views.edit_installation, name='installation-insert'),
    path('installation/new/<int:pk>', views.edit_installation, name='installation-update'),
    path('installation/new/<int:pk>/<str:focus>', views.edit_installation, name='installation-update'),
    # path('installation/new/<int:id>/', views.InstallationCreate, name='installation-update'),
    path('installation/delete/<int:id>/', views.InstallationDelete, name='installation-delete'),
    path('installation/list/', views.InstallationList, name='installation-list'),
    path('installation/list/adv/', views.InstallationListView.as_view(), name='installation-advancedsearch'),
    path('installation/<int:pk>', views.InstallationDetailView.as_view(), name='installation-detail'),
    path('installation/duplicate/<int:id>', views.InstallationDuplicate, name='installation-duplicate'),
    # url(r'^evidence/new/$', views.EvidenceCreatView.as_view(), name='evidence-insert'),
    path('evidence/new/', views.edit_evidence, name='evidence-insert'),
    path('evidence/new/<str:view>/', views.edit_evidence, name='evidence-insert'),
    path('evidence/new/<int:pk>', views.edit_evidence, name='evidence-update'),
    path('evidence/new/<int:pk>/<str:focus>', views.edit_evidence, name='evidence-update'),
    url(r'^evidence/delete/(?P<pk>\d+)/$', views.EvidenceDeleteView.as_view(), name='evidence-delete'),
    path('evidence/list', views.EvidenceListView.as_view(), name='evidence-list'),
    path('evidence/<int:pk>', views.EvidenceDetailView.as_view(), name='evidence-detail'),
    path('watersystem/new/', views.WaterSystemCreatView.as_view(), name='watersystem-insert'),
    path('watersystem/new/<str:view>/', views.WaterSystemCreatView.as_view(), name='watersystem-insert'),
    path('watersystem/new/<int:pk>', views.WaterSystemUpdateView.as_view(), name='watersystem-update'),
    url(r'^watersystem/delete/(?P<pk>\d+)/$', views.WaterSystemDeleteView.as_view(), name='watersystem-delete'),
    path('watersystem/list', views.WaterSystemListView.as_view(), name='watersystem-list'),
    path('purpose/new/<str:view>/', views.PurposeCreatView.as_view(), name='purpose-insert'),
    url(r'^purpose/new/$', views.PurposeCreatView.as_view(), name='purpose-insert'),
    path('purpose/new/<int:pk>', views.PurposeUpdateView.as_view(), name='purpose-update'),
    url(r'^purpose/delete/(?P<pk>\d+)/$', views.PurposeDeleteView.as_view(), name='purpose-delete'),
    path('purpose/list', views.PurposeListView.as_view(), name='purpose-list'),
    path('institutiontype/new/', views.InstitutionTypeCreatView.as_view(), name='institutiontype-insert'),
    path('institutiontype/new/<str:view>/', views.InstitutionTypeCreatView.as_view(), name='institutiontype-insert'),
    path('institutiontype/new/<int:pk>', views.InstitutionTypeUpdateView.as_view(), name='institutiontype-update'),
    url(r'^institutiontype/delete/(?P<pk>\d+)/$', views.InstitutionTypeDeleteView.as_view(), name='institutiontype-delete'),
    path('institutiontype/list', views.InstitutionTypeListView.as_view(), name='institutiontype-list'),
    path('religion/new/', views.ReligionCreatView.as_view(), name='religion-insert'),
    path('religion/new/<str:view>/', views.ReligionCreatView.as_view(), name='religion-insert'),
    path('religion/new/<int:pk>', views.ReligionUpdateView.as_view(), name='religion-update'),
    url(r'^religion/delete/(?P<pk>\d+)/$', views.ReligionDeleteView.as_view(), name='religion-delete'),
    path('religion/list', views.ReligionListView.as_view(), name='religion-list'),

    path('neighbourhood/new/', views.NeighbourhoodCreatView.as_view(), name='neighbourhood-insert'),
    path('neighbourhood/new/<str:view>/', views.NeighbourhoodCreatView.as_view(), name='neighbourhood-insert'),
    path('neighbourhood/new/<int:pk>', views.NeighbourhoodUpdateView.as_view(), name='neighbourhood-update'),
    url(r'^neighbourhood/delete/(?P<pk>\d+)/$', views.NeighbourhoodDeleteView.as_view(), name='neighbourhood-delete'),
    path('neighbourhood/list', views.NeighbourhoodListView.as_view(), name='neighbourhood-list'),

    # Relations
    # ------------------------------------------------------------------------------------------------------------------
    url(r'^citypersonrelation/new/$', views.CityPersonRelationCreatView.as_view(), name='citypersonrelation-insert'),
    path('citypersonrelation/new/<int:pk>', views.CityPersonRelationUpdateView.as_view(), name='citypersonrelation-update'),
    url(r'^citypersonrelation/delete/(?P<pk>\d+)/$', views.CityPersonRelationDeleteView.as_view(), name='citypersonrelation-delete'),
    path('citypersonrelation/list', views.CityPersonRelationListView.as_view(), name='citypersonrelation-list'),
    url(r'^personinstitutionrelation/new/$', views.PersonInstitutionRelationCreatView.as_view(), name='personinstitutionrelation-insert'),
    path('personinstitutionrelation/new/<int:pk>', views.PersonInstitutionRelationUpdateView.as_view(), name='personinstitutionrelation-update'),
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

    # Accessory
    # ------------------------------------------------------------------------------------------------------------------
    path('accessory/', views.Accessory, name='accessory'),
]