from django.shortcuts import render
from certifications.models import Certification

# Create your views here.
def certification_index(request):
    certifications = Certification.objects.all().order_by('-issue_date').values()
    context = {
        'certifications': certifications
    }
    return render(request, 'certification_index.html', context)

def certification_detail(request):
    return render(request, 'certification_detail.html')