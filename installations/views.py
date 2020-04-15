from django.shortcuts import render, redirect
from .forms import CityForm
from .models import City


# Create your views here.

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
    city = City.objects.get(pk=id)
    city.delete()
    return redirect('installations:city-list')