from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import House, Person
from datetime import datetime


def home(request):
    return render(request, 'index.html', {})


def persons(request):
    if request.method == 'POST' and 'createPerson' in request.POST:
        if House.objects.filter(id=request.POST.get('house')).count() == 0:
            print("Nem létező házhoz rendelés")
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("persons"))
        try:
            birthDate = datetime.strptime(request.POST.get('birth'), "%Y-%m-%d")
        except ValueError:
            print("Rossz dátum formátum")
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("persons"))
        Person.objects.create(house=House.objects.filter(id=request.POST.get('house'))[0],
                              name=request.POST.get('name'),
                              gender=request.POST.get('gender'),
                              birth=birthDate)
        return HttpResponseRedirect(reverse("persons"))
    return render(request, 'persons.html', {'data': Person.objects.all()})


def houses(request):
    if request.method == 'POST' and 'createHouse' in request.POST:
        if House.objects.filter(address=request.POST.get('address')).count() != 0:
            print("Unique constraint megsértése")
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("houses"))
        House.objects.create(address=request.POST.get('address'), houseType=request.POST.get('houseType'))
        return HttpResponseRedirect(reverse("houses"))
    return render(request, 'houses.html', {'data': House.objects.all()})


def addTestPerson(request):
    Person.objects.create(house=House(id=1),
                          name='Kiss Béla',
                          gender='férfi',
                          birth=datetime.strptime('1990-01-01', "%Y-%m-%d"))
    return HttpResponseRedirect(reverse("persons"))


def addTestHouse(request):
    House.objects.create(address='Cím', houseType='Kertes')
    return HttpResponseRedirect(reverse("houses"))
