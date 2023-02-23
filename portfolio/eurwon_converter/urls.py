from django.urls import path
from . import views

urlpatterns = [
    path('', views.eurwon_converter_index, name='eurwon_converter_index'),
]