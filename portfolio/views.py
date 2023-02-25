from django.shortcuts import render
from .models import Certification, Project

def portfolio_bio(request):
    return render(request, 'bio.html')

def portfolio_projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'project_index.html', context)

def portfolio_projects_detail(request, pk):
    project = Project.objects.get(pk=pk)
    context = {
        'project': project
    }
    return render(request, 'project_detail.html', context)

def portfolio_certifications(request):
    certifications = Certification.objects.all().order_by('-issue_date').values()
    context = {
        'certifications': certifications
    }
    return render(request, 'certification_index.html', context)

def portfolio_certifications_detail(request):
    return render(request, 'certification_detail.html')
    # Not yet implemented