from django.contrib import admin
from .models import Country, City, Citymap, Politicalorientation, Religiousorientation,Person, CityPersonRelation, Watersystem, Installation, PersonInstallationRelation, CityInistallationRelation, Organization, Organizationtype, PersonOrganizationRelation
# Register your models here.


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Citymap)
admin.site.register(Politicalorientation)
admin.site.register(Religiousorientation)
admin.site.register(Person)
admin.site.register(CityPersonRelation)
admin.site.register(Watersystem)
admin.site.register(Installation)
admin.site.register(PersonInstallationRelation)
admin.site.register(CityInistallationRelation)
admin.site.register(Organization)
admin.site.register(Organizationtype)
admin.site.register(PersonOrganizationRelation)

