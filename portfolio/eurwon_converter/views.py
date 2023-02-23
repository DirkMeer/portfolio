from django.shortcuts import render
from certifications.models import Certification

# Create your views here.
def eurwon_converter_index(request):
    return render(request, 'eurwon_converter_index.html')