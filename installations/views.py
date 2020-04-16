from django.shortcuts import render, redirect, get_object_or_404
from .forms import CityForm, InstitutionForm
from .models import City, Institution


# Create your views here.

def Home(request):
    return render(request, 'installations/home.html')

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

def CityDelete(request, id):
    city = get_object_or_404(City, pk=id)
    city.delete()
    return redirect('installations:city-list')


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
        return redirect('installations:institution-list')  # after save redirect to the city list


def InstitutionList(request):
    context = {'institution_list': Institution.objects.all()}
    return render(request, 'installations/institution_list.html', context)

def InstitutionDelete(request, id):
    institution = get_object_or_404(Institution, pk=id)
    institution.delete()
    return redirect('installations:institution-list')