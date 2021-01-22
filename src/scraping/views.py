from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from scraping.models import Vacancy
from scraping.forms import SearchForm, VForm


# Create your views here.
def home_view(request):
    form = SearchForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = SearchForm()

    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)  # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['objects_list'] = page_obj
    return render(request, 'scraping/list.html', context)


class VDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping/detail.html'
    context_object_name = 'vacancy'


class VList(ListView):
    model = Vacancy
    template_name = 'scraping/list_v.html'
    form = SearchForm()
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            print(_filter)
            qs = Vacancy.objects.filter(**_filter)
        return qs


class VCreate(CreateView):
    model = Vacancy
    form_class = VForm
    success_url = reverse_lazy('home')
    template_name = 'scraping/create.html'


class VUpdate(UpdateView):
    model = Vacancy
    form_class = VForm
    success_url = reverse_lazy('home')
    template_name = 'scraping/update.html'
