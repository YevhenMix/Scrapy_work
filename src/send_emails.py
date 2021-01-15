import os
import sys
import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from scraping_aggregator.settings import EMAIL_HOST_USER
import datetime


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_aggregator.settings"

django.setup()
from scraping.models import Vacancy, Error, Url, City, Language

today = datetime.date.today()
subject = f"Рассылка вакансий за {today} "
text_content = f"Рассылка вакансий {today}"
from_email = EMAIL_HOST_USER
ADMIN_USER = 'jeka.mixaylov58@gmail.com'


empty = '<h2>К сожалению на сегоня по вашим предпочтениям данных нет!</h2>'
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}

for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['email'])

if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    # for i in qs:
    #     vacancies.setdefault((i['city_id'], i['language_id']), [])
    #     vacancies[(i['city_id'], i['language_id'])].append(i)
    # for keys, emails in users_dct.items():
    #     rows = vacancies.get(keys, [])
    #     html = ''
    #     for row in rows:
    #         html += f'<h5><a href="{ row["url"] }">{ row["tittle"] }</a></h5>'
    #         html += f'<p> {row["description"]} </p>'
    #         html += f'<p> {row["company"]} </p><br><hr>'
    #     _html = html if html else empty
    #     for email in emails:
    #         to = email
    #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #         msg.attach_alternative(_html, 'text/html')
    #         msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p><a href="{ i["url"] }"> Error: { i["title"] }</a></p>'
    subject = f'Оштибки скрапинга за {today}'
    text_content = f'Оштибки скрапинга за {today}'

    data = error.data.get('user_data')

    if data:
        _html += '<hr>'
        _html += '<h2> Пожелания пользователей </h2>'

    for i in data:
        _html += f'<p>City: {i["city"]}, Language: {i["language"]} Email: {i["email"]}</p>'
    subject = f'Пожелания пользователей за {today}'
    text_content = f'Пожелания пользователей за {today}'


qs = Url.objects.all().values('city', 'language',)
urls_dct = {(i['city'], i['language']): True for i in qs}
urls_errors = ''

for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0] and keys[1]:
            city = City.objects.get(id=keys[0])
            language = Language.objects.get(id=keys[1])
            urls_errors += f'<p> Для города {city} и языка программирования {language} отсутсвуют урлы</a></p>'
if urls_errors:
    _html += '<hr>'
    _html += '<h2> Отсутсвующие урлы </h2>'
    subject += ' Отсутсвующие урлы'
    _html += urls_errors

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, 'text/html')
    msg.send()

