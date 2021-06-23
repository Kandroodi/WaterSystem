import django_filters
from .models import *


class InstallationFilter(django_filters.FilterSet):
    class Meta:
        model = Installation
        # fields =['name', 'watersystem__original_term']
        fields = {
            'name': ['icontains'],
            'watersystem__original_term': ['icontains'],
            'purpose__name': ['icontains'],
            'city__name': ['icontains'],
            'neighbourhood__neighbourhood_number': ['icontains'],
            'latitude': ['icontains'],
            'longitude': ['icontains'],
            'institution_as_location__name': ['icontains'],
            'secondary_literature__title': ['icontains'],
            'comment': ['icontains'],
        }
