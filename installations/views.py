from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import *
from .models import *
from django.views.generic import (View, TemplateView, ListView,
                                  DetailView, CreateView, UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from django.db.models import Q

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from utilities.views import edit_model
from utilities.views import search
from django.db.models.functions import Lower


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
            user.is_active = False
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
def CityCreate(request, id=0, view=None):
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
    if view == 'inline':
        return redirect('utilities:close')
    else:
        return redirect('installations:city-list')


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
    names = 'institutioninstitution_formset,institutionperson_formset,institutioninstallation_formset,institutionevidence_formset'
    return edit_model(request, __name__, 'Institution', 'installations', pk, formset_names=names,
                      focus=focus, view=view)


def InstitutionList(request):
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = Institution.objects.all().order_by(order_by)
    if query is not None:
        query_set = query_set.filter(
            Q(name__icontains=query) |
            Q(type__name__icontains=query) |
            Q(city__name__icontains=query)
        ).order_by(order_by)
    context = {'institution_list': query_set,
               'nentries': len(query_set),
               'query': query}
    return render(request, 'installations/institution_list.html', context)


@login_required
def InstitutionDelete(request, id):
    institution = get_object_or_404(Institution, pk=id)
    institution.delete()
    return redirect('installations:institution-list')


@login_required
def edit_person(request, pk=None, focus='', view='complete'):
    names = 'personperson_formset,personcity_formset,personneighbourhood_formset,personinstitution_formset,'
    names += 'personinstallation_formset,personevidence_formset'
    return edit_model(request, __name__, 'Person', 'installations', pk, formset_names=names,
                      focus=focus, view=view)


def PersonList(request):
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = Person.objects.all().order_by(order_by)
    context = {'person_list': query_set}
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

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        order_by = self.request.GET.get("order_by", "id")
        direction = self.request.GET.get("direction", "ascending")
        if direction == "ascending":
            query_set = self.model.objects.all().order_by(Lower(order_by))
        else:
            query_set = self.model.objects.all().order_by(Lower(order_by)).reverse()
        return query_set

    def get_context_data(self, **kwargs):
        context = super(SecondaryLiteratureListView, self).get_context_data(**kwargs)
        context["order_by"] = self.request.GET.get("order_by", "id")
        context["direction"] = self.request.GET.get("direction", "ascending")
        return context


@method_decorator(login_required, name='dispatch')
class SecondaryLiteratureCreatView(CreateView):
    model = SecondaryLiterature
    fields = '__all__'
    template_name = 'installations/secondaryliterature_form.html'

    def get_success_url(self):
        if 'view' in self.kwargs:
            viewmode = self.kwargs['view']
            if viewmode == 'inline':
                return reverse_lazy('utilities:close')
        else:
            return reverse_lazy('installations:secondaryliterature-list')


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
def edit_installation(request, pk=None, focus='', view='complete'):
    names = 'installationinstallation_formset,installationinstitution_formset,installationperson_formset,installationevidence_formset'
    return edit_model(request, __name__, 'Installation', 'installations', pk, formset_names=names,
                      focus=focus, view=view)


def InstallationList(request):
    query_set = search(request, 'installations', 'installation')
    query = request.GET.get("q", "")
    # query_set = Installation.objects.all()
    # if query is not None:
    #     query_set = query_set.filter(name__icontains=query)
    context = {'installation_list': query_set,
               'nentries': len(query_set),
               'query': query}
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

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        order_by = self.request.GET.get("order_by", "id")
        direction = self.request.GET.get("direction", "ascending")
        if direction == "ascending":
            query_set = self.model.objects.all().order_by(Lower(order_by))
        else:
            query_set = self.model.objects.all().order_by(Lower(order_by)).reverse()
        return query_set

    def get_context_data(self, **kwargs):
        context = super(EvidenceListView, self).get_context_data(**kwargs)
        context["order_by"] = self.request.GET.get("order_by", "id")
        context["direction"] = self.request.GET.get("direction", "ascending")
        return context

    # paginate_by = 10
    #
    # def get_context_data(self, **kwargs):
    #     context = super(EvidenceListView, self).get_context_data(**kwargs)
    #     evidences = self.get_queryset()
    #     page = self.request.GET.get('page')
    #     paginator = Paginator(evidences, self.paginate_by)
    #     try:
    #         evidences = paginator.page(page)
    #     except PageNotAnInteger:
    #         evidences = paginator.page(1)
    #     except EmptyPage:
    #         evidences = paginator.page(paginator.num_pages)
    #     context['evidences'] = evidences
    #     return context


@login_required
def edit_evidence(request, pk=None, focus='', view='complete'):
    names = ''
    return edit_model(request, __name__, 'Evidence', 'installations', pk, formset_names=names,
                      focus=focus, view=view)


@method_decorator(login_required, name='dispatch')
class EvidenceDeleteView(DeleteView):
    model = Evidence
    success_url = reverse_lazy("installations:evidence-list")


@method_decorator(login_required, name='dispatch')
class WaterSystemListView(ListView):
    model = Watersystem
    template_name = 'installations/watersystem_list.html'
    context_object_name = 'watersystems'

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        order_by = self.request.GET.get("order_by", "id")
        direction = self.request.GET.get("direction", "ascending")
        if direction == "ascending":
            query_set = self.model.objects.all().order_by(Lower(order_by))
        else:
            query_set = self.model.objects.all().order_by(Lower(order_by)).reverse()
        return query_set

    def get_context_data(self, **kwargs):
        context = super(WaterSystemListView, self).get_context_data(**kwargs)
        context["order_by"] = self.request.GET.get("order_by", "id")
        context["direction"] = self.request.GET.get("direction", "ascending")
        return context


@method_decorator(login_required, name='dispatch')
class WaterSystemCreatView(CreateView):
    model = Watersystem
    form_class = WatersystemForm
    template_name = 'installations/watersystem_form.html'

    def get_success_url(self):
        if 'view' in self.kwargs:
            viewmode = self.kwargs['view']
            if viewmode == 'inline':
                return reverse_lazy('utilities:close')
        else:
            return reverse_lazy('installations:watersystem-list')


@method_decorator(login_required, name='dispatch')
class WaterSystemUpdateView(UpdateView):
    model = Watersystem
    form_class = WatersystemForm
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

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        order_by = self.request.GET.get("order_by", "id")
        direction = self.request.GET.get("direction", "ascending")
        if direction == "ascending":
            query_set = self.model.objects.all().order_by(Lower(order_by))
        else:
            query_set = self.model.objects.all().order_by(Lower(order_by)).reverse()
        return query_set

    def get_context_data(self, **kwargs):
        context = super(PurposeListView, self).get_context_data(**kwargs)
        context["order_by"] = self.request.GET.get("order_by", "id")
        context["direction"] = self.request.GET.get("direction", "ascending")
        return context

@method_decorator(login_required, name='dispatch')
class PurposeCreatView(CreateView):
    model = Purpose
    fields = '__all__'
    template_name = 'installations/purpose_form.html'

    def get_success_url(self):
        if 'view' in self.kwargs:
            viewmode = self.kwargs['view']
            if viewmode == 'inline':
                return reverse_lazy('utilities:close')
        else:
            return reverse_lazy('installations:purpose-list')


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

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        order_by = self.request.GET.get("order_by", "id")
        direction = self.request.GET.get("direction", "ascending")
        if direction == "ascending":
            query_set = self.model.objects.all().order_by(Lower(order_by))
        else:
            query_set = self.model.objects.all().order_by(Lower(order_by)).reverse()
        return query_set

    def get_context_data(self, **kwargs):
        context = super(InstitutionTypeListView, self).get_context_data(**kwargs)
        context["order_by"] = self.request.GET.get("order_by", "id")
        context["direction"] = self.request.GET.get("direction", "ascending")
        return context


@method_decorator(login_required, name='dispatch')
class InstitutionTypeCreatView(CreateView):
    model = InstitutionType
    fields = '__all__'
    template_name = 'installations/institutiontype_form.html'

    def get_success_url(self):
        if 'view' in self.kwargs:
            viewmode = self.kwargs['view']
            if viewmode == 'inline':
                return reverse_lazy('utilities:close')
        else:
            return reverse_lazy('installations:institutiontype-list')


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

    def get_success_url(self):
        if 'view' in self.kwargs:
            viewmode = self.kwargs['view']
            if viewmode == 'inline':
                return reverse_lazy('utilities:close')
        else:
            return reverse_lazy('installations:religion-list')


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
    form_class = NeighbourhoodForms
    template_name = 'installations/neighbourhood_form.html'

    def get_success_url(self):
        if 'view' in self.kwargs:
            viewmode = self.kwargs['view']
            if viewmode == 'inline':
                return reverse_lazy('utilities:close')
        else:
            return reverse_lazy('installations:neighbourhood-list')  # create a list view for this if needed


@method_decorator(login_required, name='dispatch')
class NeighbourhoodListView(ListView):
    model = Neighbourhood
    template_name = 'installations/neighbourhood_list.html'
    context_object_name = 'neighbourhoods'


@method_decorator(login_required, name='dispatch')
class NeighbourhoodUpdateView(UpdateView):
    model = Neighbourhood
    fields = '__all__'
    success_url = reverse_lazy('installations:neighbourhood-list')


@method_decorator(login_required, name='dispatch')
class NeighbourhoodDeleteView(DeleteView):
    model = Neighbourhood
    success_url = reverse_lazy("installations:neighbourhood-list")


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
