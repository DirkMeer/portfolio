from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_bio, name='portfolio_bio'),
    path('projects/', views.portfolio_projects, name='portfolio_projects'),
    path(
        'projects/<int:pk>/',
        views.portfolio_projects_detail,
        name='portfolio_projects_detail'
    ),
    path('certifications/', views.portfolio_certifications, name='portfolio_certifications'),
    path(
        'certifications/<int:pk>/',
        views.portfolio_certifications_detail,
        name='portfolio_certifications_detail'
    ),
]