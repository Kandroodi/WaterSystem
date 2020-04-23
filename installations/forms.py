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
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'


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
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

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
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.form_method = 'post'  # this line sets your form's method to post
        self.helper.form_action = reverse_lazy('installations:person-insert')  # this line sets the form action
        # self.helper.layout = Layout(  # the order of the items in this layout is important
        #     'last_name',  # field1 will appear first in HTML
        #     'first_name',  # field2 will appear second in HTML
        #     'gender',
        #     'profession',
        #     'religion',
        #     'bibliography',
        #     # this is how to add the submit button to your form and since it is the last item in this tuple, it will be rendered last in the HTML
        #     Submit('submit', u'Save', css_class='btn btn-success')
        # )
        self.helper.layout = Layout(
            Fieldset(
                'first_name',  # field2 will appear second in HTML
                'gender',
                'profession',
                'religion',
                'bibliography',
            ),
            FormActions(
                        Submit('save', 'Save', css_class='btn btn-success'),
                        HTML('<a class="btn btn-default" href="person/list/">Cancel</a>')
                    )
     )

