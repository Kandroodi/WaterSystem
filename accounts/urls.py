from django.conf.urls import url
from django.urls import path
from . import views

# TEMPLATE URLS
app_name = 'accounts'

urlpatterns = [
    path('log', views.log_view, name='log_view'),
    path('logs', views.logs_view, name='logs_view'),
]
