from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(City)
admin.site.register(Citymap)
admin.site.register(Religion)
admin.site.register(Person)
admin.site.register(CityPersonRelation)
admin.site.register(Watersystem)
admin.site.register(Installation)
admin.site.register(CityInstallationRelation)
admin.site.register(Institution)
admin.site.register(InstitutionType)
admin.site.register(Bibliography)
admin.site.register(TextualEvidence)
admin.site.register(MaterialEvidence)
admin.site.register(UserProfileInfo)
