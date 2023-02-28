from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_bio, name='portfolio_bio'),
    path('projects/', views.portfolio_project_list, name='portfolio_project_list'),
    path(
        'projects/<int:pk>/',
        views.portfolio_project_detail,
        name='portfolio_project_detail'
    ),
    path('certifications/', views.portfolio_certification_list, name='portfolio_certification_list'),
    path(
        'certifications/<int:pk>/',
        views.portfolio_certification_detail,
        name='portfolio_certification_detail'
    ),
]