from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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


@login_required
def BibliographyCreate(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = BibliographyForm()
        else:
            bibliography = Bibliography.objects.get(pk=id)
            form = BibliographyForm(instance=bibliography)
        return render(request, 'installations/bibliography_form.html', {'form': form})
    else:  # request.method == "POST":
        if id == 0:
            form = BibliographyForm(request.POST)
        else:
            bibliography = Bibliography.objects.get(pk=id)
            form = BibliographyForm(request.POST, instance=bibliography)
        if form.is_valid():
            form.save()
        return redirect('installations:bibliography-list')  # after save redirect to the bibliography list


def BibliographyList(request):
    context = {'bibliography_list': Bibliography.objects.all()}
    return render(request, 'installations/bibliography_list.html', context)


@login_required
def BibliographyDelete(request, id):
    bibliography = get_object_or_404(Bibliography, pk=id)
    bibliography.delete()
    return redirect('installations:bibliography-list')


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
        return redirect('installations:installation-list')  # after save redirect to the bibliography list


def InstallationList(request):
    context = {'installation_list': Installation.objects.all()}
    return render(request, 'installations/installation_list.html', context)


@login_required
def InstallationDelete(request, id):
    installation = get_object_or_404(Installation, pk=id)
    installation.delete()
    return redirect('installations:installation-list')
