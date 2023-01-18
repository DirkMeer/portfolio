from django.urls import path
from . import views

urlpatterns = [
    path('', views.certification_index, name='certification_index'),
    path('<int:pk>/', views.certification_detail, name='certification_detail'),
]