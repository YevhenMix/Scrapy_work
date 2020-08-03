from django.shortcuts import render
from scraping.models import Vacancy
from scraping.forms import SearchForm


# Create your views here.
def home_view(request):
    form = SearchForm()

    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = Vacancy.objects.all()
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/home.html', {'objects_list': qs, 'form': form})
