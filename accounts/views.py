from django.shortcuts import render
from django.contrib.auth.models import User
from utils.view_util import Crud


# Create your views here.


def log_view(request):
    '''create a list of all update events performed by a particular user.'''
    user = User.objects.get(username=request.user.username)
    crud = Crud(user, user=True)
    var = {'crud': crud, 'page_name': 'logs'}  # {'map_name':map_name,'location_name':location_name}
    return render(request, 'accounts/log.html', var)


def logs_view(request):
    '''create a list of all update events of all users.'''
    users = User.objects.all()
    cruds = [Crud(user, user=True) for user in users]
    events = []
    for crud in cruds:
        events.extend(crud.events)
    events = sorted(events, reverse=True)
    crud.events = events[:200]
    updates = crud.updates_str
    var = {'cruds': cruds, 'page_name': 'logs', 'updates': crud.updates_str}
    return render(request, 'accounts/logs.html', var)
