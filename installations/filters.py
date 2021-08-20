import django_filters
from .models import *


class InstallationFilter(django_filters.FilterSet):
    un_name = django_filters.CharFilter(field_name='un_name', lookup_expr='icontains', label='Name')
    watersystem__original_term = django_filters.CharFilter(lookup_expr='icontains', label='Water system')
    purpose__name = django_filters.CharFilter(lookup_expr='icontains', label='Purpose')
    city__name = django_filters.CharFilter(lookup_expr='icontains', label='City')
    neighbourhood__neighbourhood_number = django_filters.CharFilter(lookup_expr='icontains',
                                                                    label='Neighbourhood number')
    institution_as_location__name = django_filters.CharFilter(lookup_expr='icontains', label='Institution as location')
    secondary_literature__title = django_filters.CharFilter(lookup_expr='icontains', label='Secondary literature')
    un_comment = django_filters.CharFilter(lookup_expr='icontains', label='Comment')

    class Meta:
        model = Installation
        # fields =['name', 'watersystem__original_term']
        fields = {

        }
