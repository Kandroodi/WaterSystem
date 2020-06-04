from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Fieldset, HTML
from django.forms import ModelForm
from django.urls import reverse_lazy

from .models import City, Institution, Person
from crispy_forms.helper import FormHelper


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
        self.helper = FormHelper()


class InstitutionForm(ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'

        labels = {
            'name': 'Institution Name'
        }

    def __init__(self, *args, **kwargs):
        super(InstitutionForm, self).__init__(*args, **kwargs)
        self.fields['bibliography'].required = False
        self.fields['textual_evidence'].required = False
        self.fields['material_evidence'].required = False
        self.fields['type'].empty_label = "Select institution type"
        self.fields['city'].empty_label = "Select city"
        self.fields['religion'].empty_label = "Select religion"
        self.fields['bibliography'].empty_label = "Select"
        self.fields['textual_evidence'].empty_label = "Select"
        self.fields['material_evidence'].empty_label = "Select"


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = False
        self.fields['bibliography'].required = False
        self.fields['religion'].empty_label = "Select religion"
        self.fields['gender'].empty_label = "Select"
