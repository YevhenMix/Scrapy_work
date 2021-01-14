from django.contrib.auth import get_user_model
from django.db import DatabaseError
from scraping.parsers import *
import os, sys
import asyncio
import datetime as dt


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_aggregator.settings"

import django
django.setup()
from scraping.models import City, Language, Vacancy, Error, Url

User = get_user_model()
parsers = ((work, 'work'),
           (rabota, 'rabota'),
           (dou, 'dou'),
           (djinni, 'djinni')
)

vacancy, errors = [], []


def get_settigs():
    qs = User.objects.filter(send_email=True).values()
    query_lst = set((q['city_id'], q['language_id']) for q in qs)
    return query_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dict[pair]
            urls.append(tmp)
    return urls


async def main(values):
    func, url, city, language = values
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    vacancy.extend(job)


setting = get_settigs()
url_lst = get_urls(setting)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_lst
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
'''for data in url_lst:
    for func, key in parsers:
        url = data['url_data'][key]
        j, e = func(url, city=data['city'], language=data['language'])
        vacancy += j
        errors += e'''

loop.run_until_complete(tasks)
loop.close()

for job in vacancy:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors: {errors}').save()


