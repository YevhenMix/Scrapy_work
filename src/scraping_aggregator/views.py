from django.shortcuts import render
import datetime


def home(request):
    name = 'Yevhen'
    date = datetime.datetime.now().date()
    cont = {'name': name, 'date': date}
    return render(request, 'home.html', cont)