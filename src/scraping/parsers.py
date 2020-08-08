import requests
from bs4 import BeautifulSoup as BS
import json
import re
from random import randint

__all__ = ('work', 'rabota', 'dou', 'djinni')

headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept': 'text/html, */*; q=0.01'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
     'Accept': 'text/html, */*; q=0.01'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
     'Accept': 'text/html, */*; q=0.01'}
]


def work(url, city=None, language=None):
    domain = 'https://www.work.ua'
    vacancy = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            resp = resp.text
            soup = BS(resp, 'html.parser')
            job_lst = soup.find('div', attrs={'id': 'pjax-job-list'}).find_all('div', attrs={'class': 'job-link'})
            if job_lst:
                for div in job_lst:
                    tittle = div.find('h2').text
                    href = div.find('h2').a['href']
                    description = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    else:
                        company = div.find('div', attrs={'class': 'add-top-xs'}).find('span').text
                    vacancy.append({'tittle': tittle, 'url': domain + href, 'description': description, 'company': company,
                                    'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'description': 'There are not job_list'})
        else:
            errors.append({'url': url, 'description': 'HTTP Response was not 200'})
    return vacancy, errors


def rabota(url, city=None, language=None):
    domain = 'https://rabota.ua'
    vacancy = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            resp = resp.text
            soup = BS(resp, 'html.parser')
            table = soup.find('table', attrs={'id': 'ctl00_content_ctl00_gridList'})
            job_lst = table.find_all('tr', attrs={'id': True})
            if job_lst:
                for tr in job_lst:
                    body = tr.find('div', attrs={'class': 'card-body'})
                    tittle = body.find('p', attrs={'class': 'card-title'}).find('a').text
                    href = body.find('p', attrs={'class': 'card-title'}).a['href']
                    description = body.find('div', attrs={'class': 'card-description'}).text
                    company = body.find('p', attrs={'class': 'company-name'}).a.text
                    vacancy.append({'tittle': tittle, 'url': domain + href, 'description': description, 'company': company,
                                    'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'description': 'There are not job_list'})
        else:
            errors.append({'url': url, 'description': 'HTTP Response was not 200'})
    return vacancy, errors


def dou(url, city=None, language=None):
    vacancy = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            resp = resp.text
            soup = BS(resp, 'html.parser')
            table = soup.find('div', attrs={'id': 'vacancyListId'}).find('ul', attrs={'class': 'lt'})
            job_lst = table.find_all('li')
            if job_lst:
                for li in job_lst:
                    tittle = li.find('div', attrs={'class': 'title'}).a.text
                    href = li.find('div', attrs={'class': 'title'}).a['href']
                    description = li.find('div', attrs={'class': 'sh-info'}).text
                    company = li.find('div', attrs={'class': 'title'}).find('strong').a.text
                    vacancy.append({'tittle': tittle, 'url': href, 'description': description, 'company': company,
                                    'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'description': 'There are not job_list'})
        else:
            errors.append({'url': url, 'description': 'HTTP Response was not 200'})
    return vacancy, errors


def djinni(url, city=None, language=None):
    domain = 'https://djinni.co'
    vacancy = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            find = r'at(\b.*\b)'
            resp = resp.text
            soup = BS(resp, 'html.parser')
            table = soup.find('div', attrs={'class': 'col-sm-8'}).find('ul', attrs={'class': 'list-jobs'})
            job_lst = table.find_all('li')
            if job_lst:
                for li in job_lst:
                    tittle = li.find('div', attrs={'class': 'list-jobs__title'}).a.text
                    href = li.find('div', attrs={'class': 'list-jobs__title'}).a['href']
                    description = li.find('div', attrs={'class': 'list-jobs__description'}).p.text
                    company = li.find('div', attrs={'class': 'list-jobs__details__info'}).text
                    company = re.findall(find, company)
                    if company:
                        company = company[0]
                    else:
                        company = 'No name'
                    vacancy.append({'tittle': tittle, 'url': domain + href, 'description': description, 'company': company,
                                    'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'description': 'There are not job_list'})
        else:
            errors.append({'url': url, 'description': 'HTTP Response was not 200'})
    return vacancy, errors


if __name__ == '__main__':
    with open('work.json', 'w') as f:
        vacancy, errors = djinni('https://djinni.co/jobs/?primary_keyword=Python&location=%D0%9A%D0%B8%D0%B5%D0%B2&title_only=True')
        json.dump(vacancy, f, indent=4)
