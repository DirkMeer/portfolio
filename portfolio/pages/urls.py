from django.urls import path
from . import views

urlpatterns = [
    path('', views.pages_home, name='pages_home'),
]