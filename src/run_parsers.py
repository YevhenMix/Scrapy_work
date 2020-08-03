from django.db import DatabaseError

from scraping.parsers import *
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_aggregator.settings"

import django
django.setup()

from scraping.models import City, Language, Vacancy

parsers = ((work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
           (rabota, 'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=Python'),
           (dou, 'https://jobs.dou.ua/vacancies/?category=Python&search=%D0%9A%D0%B8%D0%B5%D0%B2'),
           (djinni, 'https://djinni.co/jobs/?primary_keyword=Python&location=%D0%9A%D0%B8%D0%B5%D0%B2&title_only=True')
)

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()
vacancy, errors = [], []

for func, url in parsers:
    j, e = func(url)
    vacancy += j
    errors += e

for job in vacancy:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass
