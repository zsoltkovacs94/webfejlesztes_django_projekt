from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import House, Person
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    return HttpResponseRedirect(reverse("persons"))


@login_required(login_url='login')
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


@login_required(login_url='login')
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


def login(request):
    if request.method == 'POST' and 'login' in request.POST:
        print('LOGIN kérés fogadva')
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("persons"))
        else:
            print('A felhasználó nem létezik')
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("login"))
    return render(request, 'login.html', {})


def register(request):
    if request.method == 'POST' and 'register' in request.POST:
        print('REGISTER kérés fogadva')
        if User.objects.filter(username=request.POST.get('username')).exists():
            print('A felhasználó már létezik')
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("register"))
        if request.POST.get('username') == '' or\
                request.POST.get('password1') == '' or\
                request.POST.get('password2') == '' or\
                request.POST.get('email') == '':
            print('Töltse ki az összes mezőt')
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("register"))
        if request.POST.get('password1') != request.POST.get('password2'):
            print('Nem egyező jelszópár')
            #Későbbiekben helyettesíteni
            return HttpResponseRedirect(reverse("register"))
        user = User.objects.create_user(request.POST.get('username'),
                                        request.POST.get('email'),
                                        request.POST.get('password1'))
        user.save()
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'register.html', {})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("login"))
