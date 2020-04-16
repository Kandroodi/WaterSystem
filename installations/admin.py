from django.contrib import admin
from .models import City, Citymap, Religion, Person, CityPersonRelation, Watersystem, Installation
from .models import CityInistallationRelation, Institution, InstitutionnType, Bibliography, TextualEvidence, MaterialEvidence

# Register your models here.

admin.site.register(City)
admin.site.register(Citymap)
admin.site.register(Religion)
admin.site.register(Person)
admin.site.register(CityPersonRelation)
admin.site.register(Watersystem)
admin.site.register(Installation)
admin.site.register(CityInistallationRelation)
admin.site.register(Institution)
admin.site.register(InstitutionnType)
admin.site.register(Bibliography)
admin.site.register(TextualEvidence)
admin.site.register(MaterialEvidence)