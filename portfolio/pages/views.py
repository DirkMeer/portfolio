from django.shortcuts import render

# Create your views here.
def pages_home(request):
    return render(request, 'pages_home.html')