from django.forms import ModelForm
from .models import City, Institution


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'latitude', 'longitude']
        # its possible to use following line for all fields, also exclude
        # fields = '__all__'
        labels = {
            'name': 'City Name'
        }

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        # self.fields['country'].empty_label = "Select"
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False


class InstitutionForm(ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'

        labels = {
            'name': 'Institution Name'
        }

    def __init__(self, *args, **kwargs):
        super(InstitutionForm, self).__init__(*args, **kwargs)
        # self.fields['country'].empty_label = "Select"
        # self.fields['latitude'].required = False
        # self.fields['longitude'].required = False