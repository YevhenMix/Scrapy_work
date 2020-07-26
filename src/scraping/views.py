from django.shortcuts import render
from scraping.models import Vacancy


# Create your views here.
def home_view(request):
    qs = Vacancy.objects.all()
    return render(request, 'home.html', {'objects_list': qs})
