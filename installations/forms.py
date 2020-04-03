from django.forms import ModelForm
from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'country', 'latitude', 'longitude']
        # its possible to use following line for all fields, also exclude
        # fields = '__all__'