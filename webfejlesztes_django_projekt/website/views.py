from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import House, Person
from datetime import datetime


def home(request):
    return render(request, 'index.html', {})


def persons(request):
    if request.GET.get('mode'):
        mode = request.GET['mode']
    else:
        mode = 'add'
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
    if request.method == 'POST' and 'editPerson' in request.POST:
        if Person.objects.filter(id=request.POST.get('id')).count() == 0:
            print("Nem található az adott ember")
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("persons"))
        if request.POST.get('house') == '' or House.objects.filter(id=request.POST.get('house')).count() == 0:
            newHouse = Person.objects.filter(id=request.POST.get('id'))[0].house
        else:
            newHouse = House.objects.filter(id=request.POST.get('house'))[0]
        newName = request.POST.get('name')
        if newName == '':
            newName = Person.objects.filter(id=request.POST.get('id'))[0].name
        newGender = request.POST.get('gender')
        if newGender == '':
            newGender = Person.objects.filter(id=request.POST.get('id'))[0].gender
        try:
            newBirth = datetime.strptime(request.POST.get('birth'), "%Y-%m-%d")
        except ValueError:
            newBirth = Person.objects.filter(id=request.POST.get('id'))[0].birth
        Person.objects.filter(id=request.POST.get('id')).update(house=newHouse, name=newName, gender=newGender, birth=newBirth)
    if request.method == 'POST' and 'deletePerson' in request.POST:
        Person.objects.filter(id=request.POST.get('id')).delete()
    return render(request, 'persons.html', {'data': Person.objects.all(),
                                            'mode': mode})


def houses(request):
    if request.GET.get('mode'):
        mode = request.GET['mode']
    else:
        mode = 'add'
    if request.method == 'POST' and 'createHouse' in request.POST:
        if House.objects.filter(address=request.POST.get('address')).count() != 0:
            print("Unique constraint megsértése")
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("houses"))
        House.objects.create(address=request.POST.get('address'), houseType=request.POST.get('houseType'))
    if request.method == 'POST' and 'editHouse' in request.POST:
        if House.objects.filter(id=request.POST.get('id')).count() == 0:
            print("Nem található az adott ház")
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("houses"))
        newAddress = request.POST.get('address')
        if newAddress == '':
            newAddress = House.objects.filter(id=request.POST.get('id'))[0].address
        newHT = request.POST.get('houseType')
        if newHT == '':
            newHT = House.objects.filter(id=request.POST.get('id'))[0].houseType
        House.objects.filter(id=request.POST.get('id')).update(address=newAddress,
                                                                   houseType=newHT)
    if request.method == 'POST' and 'deleteHouse' in request.POST:
        House.objects.filter(id=request.POST.get('id')).delete()
    return render(request, 'houses.html', {'data': House.objects.all(),
                                           'mode': mode})


def addTestPerson(request):
    Person.objects.create(house=House(id=1),
                          name='Kiss Béla',
                          gender='férfi',
                          birth=datetime.strptime('1990-01-01', "%Y-%m-%d"))
    return HttpResponseRedirect(reverse("persons"))


def addTestHouse(request):
    House.objects.create(address='Cím', houseType='Kertes')
    return HttpResponseRedirect(reverse("houses"))
