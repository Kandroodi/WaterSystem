from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import *
from .models import *
from django.views.generic import (View, TemplateView, ListView,
                                  DetailView, CreateView, UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
import json
from django.apps import apps
import sys
import inspect
from django.contrib import messages

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from utilities.views import edit_model


# Create your views here.
def register(request):
    registered = False

    if request.method == 'POST':
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()
            # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user
            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
            # Now save model
            profile.save()
            # Registration Successful!
            registered = True
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'installations/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)
        # If we have a user
        if user:
            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page. In this case their homepage.
                return HttpResponseRedirect(reverse('installations:home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'installations/login.html', {})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('installations:home'))


# Forms and lists
def Home(request):
    return render(request, 'installations/home.html')


@login_required
def CityCreate(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = CityForm()
        else:
            city = City.objects.get(pk=id)
            form = CityForm(instance=city)
        return render(request, 'installations/city_form.html', {'form': form})
    else:  # request.method == "POST":
        if id == 0:
            form = CityForm(request.POST)
        else:
            city = City.objects.get(pk=id)
            form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
        return redirect('installations:city-list')  # after save redirect to the city list


def CityList(request):
    context = {'city_list': City.objects.all()}
    return render(request, 'installations/city_list.html', context)


@login_required
def CityDelete(request, id):
    city = get_object_or_404(City, pk=id)
    city.delete()
    return redirect('installations:city-list')


@login_required
def edit_institution(request, pk=None, focus='', view='complete'):
    names = 'institutioninstallation_formset'
    return edit_model(request, __name__, 'Institution', 'installations', pk, formset_names=names,
                      focus=focus, view=view)


def InstitutionCreate(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = InstitutionForm()
        else:
            institution = Institution.objects.get(pk=id)
            form = InstitutionForm(instance=institution)
        return render(request, 'installations/institution_form.html', {'form': form})
    else:  # request.method == "POST":
        if id == 0:
            form = InstitutionForm(request.POST)
        else:
            institution = Institution.objects.get(pk=id)
            form = InstitutionForm(request.POST, instance=institution)
        if form.is_valid():
            form.save()
        return redirect('installations:institution-list')  # after save redirect to the institution list


def InstitutionList(request):
    context = {'institution_list': Institution.objects.all()}
    return render(request, 'installations/institution_list.html', context)


@login_required
def InstitutionDelete(request, id):
    institution = get_object_or_404(Institution, pk=id)
    institution.delete()
    return redirect('installations:institution-list')


@login_required
def PersonCreateNew(request, pk=None, focus='', view='complete'):
    names = 'personcity_formset,personneighbourhood_formset,personinstitution_formset,personinstallation_formset,personevidence_formset'
    name_space = __name__
    model_name = 'Person'
    app_name = 'installations'
    instance_id = None
    focus = ''
    view = 'complete'

    model = apps.get_model(app_name, model_name)
    modelform = get_modelform(name_space, model_name + 'Form')
    instance = model.objects.get(pk=instance_id) if instance_id else None
    crud = Crud(instance) if instance else None
    ffm, form = None, None
    if request.method == 'POST':
        focus, button = getfocus(request), getbutton(request)
        if button in 'delete,cancel,confirm_delete':
            return delete_model(request, name_space, model_name, app_name, instance_id)
        if button == 'saveas' and instance: instance = copy_complete(instance)
        form = modelform(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            print('form is valid: ', form.cleaned_data, type(form))
            instance = form.save()
            if view == 'complete':
                ffm = FormsetFactoryManager(name_space, names, request, instance)
                valid = ffm.save()
                if valid:
                    show_messages(request, button, model_name)
                    if button == 'add_another':
                        return HttpResponseRedirect(reverse(app_name + ':add_' + model_name.lower()))
                    return HttpResponseRedirect(reverse(
                        app_name + ':edit_' + model_name.lower(),
                        kwargs={'pk': instance.pk, 'focus': focus}))
                else:
                    print('ERROR', ffm.errors)
            else:
                return HttpResponseRedirect('/utilities/close/')
    if not form: form = modelform(instance=instance)
    if not ffm: ffm = FormsetFactoryManager(name_space, names, instance=instance)
    tabs = make_tabs(model_name.lower(), focus_names=focus)
    page_name = 'person_form'
    # page_name = 'Edit ' + model_name.lower() if instance_id else 'Add ' + model_name.lower()
    args = {'form': form, 'page_name': page_name, 'crud': crud,
            'tabs': tabs, 'view': view}
    args.update(ffm.dict)
    return render(request, app_name + '/person_form' + '.html', args)

@login_required
def edit_person(request, pk=None, focus='', view='complete'):
    names = 'personcity_formset,personneighbourhood_formset,personinstitution_formset,'
    names += 'personinstallation_formset,personevidence_formset'
    return edit_model(request, __name__, 'Person', 'installations', pk, formset_names=names,
                      focus=focus, view=view)


@login_required
def PersonCreate(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = PersonForm()
        else:
            person = Person.objects.get(pk=id)
            form = PersonForm(instance=person)
        return render(request, 'installations/person_form.html', {'form': form})
    else:  # request.method == "POST":
        if id == 0:
            form = PersonForm(request.POST)
        else:
            person = Person.objects.get(pk=id)
            form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
        return redirect('installations:person-list')  # after save redirect to the Person list


def PersonList(request):
    context = {'person_list': Person.objects.all()}
    return render(request, 'installations/person_list.html', context)


@login_required
def PersonDelete(request, id):
    person = get_object_or_404(Person, pk=id)
    person.delete()
    return redirect('installations:person-list')


@method_decorator(login_required, name='dispatch')
class SecondaryLiteratureListView(ListView):
    model = SecondaryLiterature
    template_name = 'installations/secondaryliterature_list.html'
    context_object_name = 'secondaryliteratures'


@method_decorator(login_required, name='dispatch')
class SecondaryLiteratureCreatView(CreateView):
    model = SecondaryLiterature
    fields = '__all__'
    template_name = 'installations/secondaryliterature_form.html'
    success_url = reverse_lazy('installations:secondaryliterature-list')


@method_decorator(login_required, name='dispatch')
class SecondaryLiteratureUpdateView(UpdateView):
    model = SecondaryLiterature
    fields = '__all__'
    success_url = reverse_lazy('installations:secondaryliterature-list')


@method_decorator(login_required, name='dispatch')
class SecondaryLiteratureDeleteView(DeleteView):
    model = SecondaryLiterature
    success_url = reverse_lazy("installations:secondaryliterature-list")


@login_required
def InstallationCreate(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = InstallationForm()
        else:
            installation = Installation.objects.get(pk=id)
            form = InstallationForm(instance=installation)
        return render(request, 'installations/installation_form.html', {'form': form})
    else:  # request.method == "POST":
        if id == 0:
            form = InstallationForm(request.POST)
        else:
            installation = Installation.objects.get(pk=id)
            form = InstallationForm(request.POST, instance=installation)
        if form.is_valid():
            form.save()
        return redirect('installations:installation-list')  # after save redirect to the installation list


def InstallationList(request):
    context = {'installation_list': Installation.objects.all()}
    return render(request, 'installations/installation_list.html', context)


@login_required
def InstallationDelete(request, id):
    installation = get_object_or_404(Installation, pk=id)
    installation.delete()
    return redirect('installations:installation-list')


# Using Class based View

@method_decorator(login_required, name='dispatch')
class EvidenceListView(ListView):
    model = Evidence
    template_name = 'installations/evidence_list'
    context_object_name = 'evidences'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EvidenceListView, self).get_context_data(**kwargs)
        evidences = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(evidences, self.paginate_by)
        try:
            evidences = paginator.page(page)
        except PageNotAnInteger:
            evidences = paginator.page(1)
        except EmptyPage:
            evidences = paginator.page(paginator.num_pages)
        context['evidences'] = evidences
        return context


@method_decorator(login_required, name='dispatch')
class EvidenceCreatView(CreateView):
    model = Evidence
    # fields = ('title', 'author', 'date', 'secondary_literature', 'description')
    fields = '__all__'
    template_name = 'installations/evidence_form.html'
    success_url = reverse_lazy('installations:evidence-list')


@method_decorator(login_required, name='dispatch')
class EvidenceUpdateView(UpdateView):
    # fields = '__all__'
    model = Evidence
    form_class = EvidenceForm
    success_url = reverse_lazy('installations:evidence-list')

    ## if you want to see the detail of updated record you can add a detail view and reverse there. uncomment the following lines
    # def get_success_url(self):
    #     return reverse_lazy('installations:textualevidence-detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class EvidenceDeleteView(DeleteView):
    model = Evidence
    success_url = reverse_lazy("installations:evidence-list")


@method_decorator(login_required, name='dispatch')
class WaterSystemListView(ListView):
    model = Watersystem
    template_name = 'installations/watersystem_list.html'
    context_object_name = 'watersystems'


@method_decorator(login_required, name='dispatch')
class WaterSystemCreatView(CreateView):
    model = Watersystem
    fields = '__all__'
    template_name = 'installations/watersystem_form.html'
    success_url = reverse_lazy('installations:watersystem-list')


@method_decorator(login_required, name='dispatch')
class WaterSystemUpdateView(UpdateView):
    model = Watersystem
    fields = '__all__'
    success_url = reverse_lazy('installations:watersystem-list')


@method_decorator(login_required, name='dispatch')
class WaterSystemDeleteView(DeleteView):
    model = Watersystem
    success_url = reverse_lazy("installations:watersystem-list")


@method_decorator(login_required, name='dispatch')
class PurposeListView(ListView):
    model = Purpose
    template_name = 'installations/purpose_list.html'
    context_object_name = 'purposes'


@method_decorator(login_required, name='dispatch')
class PurposeCreatView(CreateView):
    model = Purpose
    fields = '__all__'
    template_name = 'installations/purpose_form.html'
    success_url = reverse_lazy('installations:purpose-list')


@method_decorator(login_required, name='dispatch')
class PurposeUpdateView(UpdateView):
    model = Purpose
    fields = '__all__'
    success_url = reverse_lazy('installations:purpose-list')


@method_decorator(login_required, name='dispatch')
class PurposeDeleteView(DeleteView):
    model = Purpose
    success_url = reverse_lazy("installations:purpose-list")


@method_decorator(login_required, name='dispatch')
class InstitutionTypeListView(ListView):
    model = InstitutionType
    template_name = 'installations/institutiontype_list.html'
    context_object_name = 'institutiontypes'


@method_decorator(login_required, name='dispatch')
class InstitutionTypeCreatView(CreateView):
    model = InstitutionType
    fields = '__all__'
    template_name = 'installations/institutiontype_form.html'
    success_url = reverse_lazy('installations:institutiontype-list')


@method_decorator(login_required, name='dispatch')
class InstitutionTypeUpdateView(UpdateView):
    model = InstitutionType
    fields = '__all__'
    success_url = reverse_lazy('installations:institutiontype-list')


@method_decorator(login_required, name='dispatch')
class InstitutionTypeDeleteView(DeleteView):
    model = InstitutionType
    success_url = reverse_lazy("installations:institutiontype-list")


@method_decorator(login_required, name='dispatch')
class ReligionListView(ListView):
    model = Religion
    template_name = 'installations/religion_list.html'
    context_object_name = 'religions'


@method_decorator(login_required, name='dispatch')
class ReligionCreatView(CreateView):
    model = Religion
    fields = '__all__'
    template_name = 'installations/religion_form.html'
    success_url = reverse_lazy('installations:religion-list')


@method_decorator(login_required, name='dispatch')
class ReligionUpdateView(UpdateView):
    model = Religion
    fields = '__all__'
    success_url = reverse_lazy('installations:religion-list')


@method_decorator(login_required, name='dispatch')
class ReligionDeleteView(DeleteView):
    model = Religion
    success_url = reverse_lazy("installations:religion-list")


@method_decorator(login_required, name='dispatch')
class NeighbourhoodCreatView(CreateView):
    model = Neighbourhood
    fields = '__all__'
    template_name = 'installations/neighbourhood_form.html'
    success_url = reverse_lazy('installations:home')


# Relations
# ----------------------------------------------------------------------------------------------------------------------
# CityPersonRelation
@method_decorator(login_required, name='dispatch')
class CityPersonRelationListView(ListView):
    model = CityPersonRelation
    template_name = 'installations/citypersonrelation_list.html'
    context_object_name = 'citypersonrelations'


@method_decorator(login_required, name='dispatch')
class CityPersonRelationCreatView(CreateView):
    model = CityPersonRelation
    fields = '__all__'
    template_name = 'installations/citypersonrelation_form.html'
    success_url = reverse_lazy('installations:citypersonrelation-list')


@method_decorator(login_required, name='dispatch')
class CityPersonRelationUpdateView(UpdateView):
    model = CityPersonRelation
    fields = '__all__'
    success_url = reverse_lazy('installations:citypersonrelation-list')


@method_decorator(login_required, name='dispatch')
class CityPersonRelationDeleteView(DeleteView):
    model = CityPersonRelation
    success_url = reverse_lazy("installations:citypersonrelation-list")


# PersonInstitutionRelation
@method_decorator(login_required, name='dispatch')
class PersonInstitutionRelationListView(ListView):
    model = PersonInstitutionRelation
    template_name = 'installations/personinstitutionrelation_list.html'
    context_object_name = 'personinstitutionrelations'


@method_decorator(login_required, name='dispatch')
class PersonInstitutionRelationCreatView(CreateView):
    model = PersonInstitutionRelation
    fields = '__all__'
    template_name = 'installations/personinstitutionrelation_form.html'
    success_url = reverse_lazy('installations:personinstitutionrelation-list')


@method_decorator(login_required, name='dispatch')
class PersonInstitutionRelationUpdateView(UpdateView):
    model = PersonInstitutionRelation
    fields = '__all__'
    success_url = reverse_lazy('installations:personinstitutionrelation-list')


@method_decorator(login_required, name='dispatch')
class PersonInstitutionRelationDeleteView(DeleteView):
    model = PersonInstitutionRelation
    success_url = reverse_lazy("installations:personinstitutionrelation-list")


# PersonInstallationRelation
@method_decorator(login_required, name='dispatch')
class PersonInstallationRelationListView(ListView):
    model = PersonInstallationRelation
    template_name = 'installations/personinstallationrelation_list.html'
    context_object_name = 'personinstallationrelations'


@method_decorator(login_required, name='dispatch')
class PersonInstallationRelationCreatView(CreateView):
    model = PersonInstallationRelation
    fields = '__all__'
    template_name = 'installations/personinstallationrelation_form.html'
    success_url = reverse_lazy('installations:personinstallationrelation-list')


@method_decorator(login_required, name='dispatch')
class PersonInstallationRelationUpdateView(UpdateView):
    model = PersonInstallationRelation
    fields = '__all__'
    success_url = reverse_lazy('installations:personinstallationrelation-list')


@method_decorator(login_required, name='dispatch')
class PersonInstallationRelationDeleteView(DeleteView):
    model = PersonInstallationRelation
    success_url = reverse_lazy("installations:personinstallationrelation-list")


# CityInistallationRelation
@method_decorator(login_required, name='dispatch')
class CityInstallationRelationListView(ListView):
    model = CityInstallationRelation
    template_name = 'installations/cityinstallationrelation_list.html'
    context_object_name = 'cityinstallationrelations'


@method_decorator(login_required, name='dispatch')
class CityInstallationRelationCreatView(CreateView):
    model = CityInstallationRelation
    fields = '__all__'
    template_name = 'installations/cityinstallationrelation_form.html'
    success_url = reverse_lazy('installations:cityinstallationrelation-list')


@method_decorator(login_required, name='dispatch')
class CityInstallationRelationUpdateView(UpdateView):
    model = CityInstallationRelation
    fields = '__all__'
    success_url = reverse_lazy('installations:cityinstallationrelation-list')


@method_decorator(login_required, name='dispatch')
class CityInstallationRelationDeleteView(DeleteView):
    model = CityInstallationRelation
    success_url = reverse_lazy("installations:cityinstallationrelation-list")


# Functions
def get_modelform(namespace, modelform_name):
    temp = sys.modules[namespace]
    classes = dict(inspect.getmembers(temp, inspect.isclass))
    try:
        return classes[modelform_name]
    except:
        raise ValueError(
            'could not find', modelform_name, 'in', classes, 'did you import it?')


class Crud:
    def __init__(self, instance, related_name='', add_related_events=True, user=False):
        i = instance
        self.instance = instance
        self.related_name = related_name
        self.add_related_events = add_related_events
        self.user = user
        self.model_name = str(type(i)).split('.')[-1].split("'")[0].lower()
        self.app_name = str(type(i)).split('.')[0].split("'")[-1].lower()
        if user:
            self.get_user_crud_events()
        else:
            self.get_crud_events()
        if add_related_events: self._add_related_events()

    def get_user_crud_events(self):
        events = CRUDEvent.objects.filter(
            user__username=self.instance.username)
        self._get_crud_events(events)

    def get_crud_events(self):
        events = CRUDEvent.objects.filter(
            content_type__model=self.model_name, object_id=self.instance.pk)
        self._get_crud_events(events)

    def _get_crud_events(self, events):
        o = []
        for e in events:
            if self.user:
                o.append(e)
            elif e.get_event_type_display() == 'Create':
                o.append(e)
            elif not e.changed_fields:
                e.delete()
            else:
                o.append(e)  # store
        self.events = [Event(e, self.related_name, self.instance) for e in o]

    def _add_related_events(self):
        self.cruds = []
        for attr in dir(self.instance):
            if 'relation_set' in attr and not attr.startswith('_'):
                cruds = [Crud(ri, instance2name(ri), False) for ri in
                         getattr(self.instance, attr).all()]
                self.cruds.extend(cruds)
            if attr == 'relations':
                for r in self.instance.relations.through.objects.all():
                    if hasattr(r, 'primary'):
                        pk1, pk2 = r.primary.pk, r.secondary.pk
                    elif hasattr(r, 'container'):
                        pk1, pk2 = r.container.pk, r.contained.pk
                    else:
                        continue
                    if self.instance.pk in [pk1, pk2]:
                        self.cruds.append(Crud(r, instance2name(r)))

    def __lt__(self, other):
        if len(self.events) == 0: return True
        if len(other.events) == 0: return False
        return self.events[0].epoch < other.events[0].epoch

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ' // '.join([self.app_name, self.model_name, self.last_update])

    @property
    def contributers(self):
        return ' | '.join([e.user.username for e in self.events])

    @property
    def created(self):
        for e in self.events:
            if e.type == 'Create':
                return e.username + ' ' + e.time_str
        return 'user unknown'

    def _make_change_fields_string(self, e):  # changed_fields):
        m = ''
        if self.user:
            if e.type == 'Create': return ['created a ' + e.model_name + ': ' + e.object_str]
            m = e.model_name + ': ' + e.object_str + ' | '
        elif not e.changed and not e.related_name:
            return ['no changes']
        o = []
        for change in e.changes:
            if change.field == 'last_login':
                o.append('login')
            elif change.field == 'date_joined':
                pass
            else:
                o.append(m + change.field + ': ' + change.old_state + ' -> ' + change.new_state)
        return o

    @property
    def username(self):
        return self.events[0].username

    @property
    def updates(self):
        events = []
        if self.related_name or self.user:
            events = [e for e in self.events]
        else:
            events = [e for e in self.events if e.type == 'Update']
        if self.add_related_events:
            for crud in self.cruds:
                events.extend(crud.events)
        return sorted(events, reverse=True)

    @property
    def anychanges(self):
        return True if self.updates else False

    @property
    def updates_str_hide_user(self):
        return self._updates_str(show_user=False)

    @property
    def updates_str(self):
        return self._updates_str()

    def _updates_str(self, show_user=True):
        o = []
        for e in self.updates:
            cfs = self._make_change_fields_string(e)
            for cf in cfs:
                line = [e.username, e.time_str, cf] if show_user else [e.time_str, cf]
                o.append([' | '.join(line), e.link])
        if o == []: return 'no updates'
        return o

    @property
    def last_update(self):
        events = self.updates
        if len(events) == 0: return 'unknown'
        e = events[0]
        if len(events) == 1 and e.type == 'Create':
            cf = 'created'
        else:
            cf = ' | '.join(self._make_change_fields_string(e))
        return ' // '.join([e.time_str, e.username, cf])

    @property
    def last_update_time(self):
        if len(self.events) == 0: return 'time unknown'
        return self.events[0].time_str

    @property
    def last_update_by(self):
        if len(self.events) == 0: return 'user unknown'
        return self.events[0].username


def getfocus(request):
    '''extracts focus variable from the request object to correctly set the active tabs.'''
    if 'focus' in request.POST.keys():
        return request.POST['focus']
    else:
        return 'default'


def getbutton(request):
    if 'save' in request.POST.keys():
        return request.POST['save']
    else:
        return 'default'


def show_messages(request, button, model_name):
    '''provide user feedback on submitting a form.'''
    if button == 'saveas':
        messages.warning(request,
                         'saved a copy of ' + model_name + '. Use "save" button to store edits to this copy')
    elif button == 'confirm_delete':
        messages.success(request, model_name + ' deleted')
    elif button == 'cancel':
        messages.warning(request, 'delete aborted')
    else:
        messages.success(request, model_name + ' saved')


class FormsetFactoryManager:
    '''object that hold formset factories and corresponding names.
    use case: and add/edit view uses many formsets these can be created
    with this class by providing a list of names of the formset factory functions
    the formsets are stored in formset variable and the dict variable contains
    a name / formset to update the var variable provided for the template
    (names can be used in the template to acces the formsets)
    '''

    def __init__(self, name_space, names, request=None, instance=None):
        '''
        names_sp 	__name__
        names 		csv or list of names, should correspond to formset factories
                    imported in the module calling this class
        request 	django request variable
        instance 	instance of model that is updated
        '''
        self.names = names.split(',') if type(names) == str else names
        self.formset_factories = [get_modelform(name_space, name)
                                  for name in self.names if name != '']
        if request == None:
            self.formsets = [ff(instance=instance) for ff in self.formset_factories]
        else:
            self.formsets = [ff(request.POST, request.FILES, instance=instance)
                             for ff in self.formset_factories]
        self.dict = dict([[name, fs] for name, fs in zip(self.names, self.formsets)])

    def __repr__(self):
        return ' '.join(self.names)

    def save(self):
        self.valid, self.errors = True, []
        for formset in self.formsets:
            if formset.is_valid():
                formset.save()
            else:
                self.valid = False
                self.errors.append(formset.errors)
        return self.valid


class Tab:
    def __init__(self, tab_names, focus=0):
        if type(tab_names) != list:
            self.tab_names = tab_names.split(',')
        else:
            self.tab_names = tab_names
        self.ntabs = len(self.tab_names)
        self.focus = self.tab_names[focus]
        if focus >= self.ntabs: self.focus = self.tab_names[0]

    def __repr__(self):
        return ' '.join(self.tab_names)


class Tabs:
    def __init__(self, tabs, names, focus_names=''):
        self.tabs = tabs
        if type(names) != list:
            self.names = names.split(',')
        else:
            self.names = names
        for name, tab in zip(self.names, self.tabs):
            setattr(self, name, tab)
        if focus_names:
            if type(focus_names) != list:
                self.focus = focus_names.split(',')
            else:
                self.focus = focus_names
        else:
            self.focus = [t.focus for t in self.tabs]


def make_tabs(tab_type, focus=0, focus_names=''):
    minimize = Tab('Edit,Minimize', focus)
    print(tab_type)
    if focus_names == 'default': focus_names = ''
    if tab_type == 'person':
        t = 'Citys, Neighbourhoods, Institutions, Installations, Evidences'
        relations = Tab(t, focus)
        return Tabs([minimize, relations], 'minimize,relations', focus_names)
