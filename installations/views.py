from django.shortcuts import render
from .forms import  CityForm

# Create your views here.

def CityCreate(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_item = form.save(commit=False)
            city_item.save()
    else:
        form = CityForm()
    return render(request, 'installations/city_form.html', {'form': form})