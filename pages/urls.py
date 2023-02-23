from django.urls import path
from . import views
from projects import views as projects

urlpatterns = [
    path('', projects.project_index, name='project_index'),
    path('home/', views.pages_home, name='pages_home'),
]