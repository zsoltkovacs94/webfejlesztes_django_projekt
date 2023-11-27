from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import House, Person
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
        if request.POST.get('house') == '' or\
                request.POST.get('name') == '' or\
                request.POST.get('gender') == '':
            messages.error(request, 'Leave no fields empty')
            return HttpResponseRedirect(reverse("persons"))
        if House.objects.filter(id=request.POST.get('house')).count() == 0:
            messages.error(request, 'Given House ID doesn\'t exist')
            return HttpResponseRedirect(reverse("persons"))
        try:
            birthDate = datetime.strptime(request.POST.get('birth'), "%Y-%m-%d")
        except ValueError:
            messages.error(request, 'Wrong date format')
            return HttpResponseRedirect(reverse("persons"))
        Person.objects.create(house=House.objects.filter(id=request.POST.get('house'))[0],
                              name=request.POST.get('name'),
                              gender=request.POST.get('gender'),
                              birth=birthDate)
        messages.success(request, 'Create successful')
    if request.method == 'POST' and 'editPerson' in request.POST:
        if Person.objects.filter(id=request.POST.get('id')).count() == 0:
            messages.error(request, 'Given person doesn\'t exist')
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
        messages.success(request, 'Edit successful')
    if request.method == 'POST' and 'deletePerson' in request.POST:
        Person.objects.filter(id=request.POST.get('id')).delete()
        messages.success(request, 'Delete successful')
    return render(request, 'persons.html', {'data': Person.objects.all(),
                                            'mode': mode})


@login_required(login_url='login')
def houses(request):
    if request.GET.get('mode'):
        mode = request.GET['mode']
    else:
        mode = 'add'
    if request.method == 'POST' and 'createHouse' in request.POST:
        if request.POST.get('address') == '' or\
                request.POST.get('houseType') == '':
            messages.error(request, 'Leave no fields empty')
            return HttpResponseRedirect(reverse("houses"))
        if House.objects.filter(address=request.POST.get('address')).count() != 0:
            messages.error(request, 'Address must be unique')
            return HttpResponseRedirect(reverse("houses"))
        House.objects.create(address=request.POST.get('address'), houseType=request.POST.get('houseType'))
        messages.success(request, 'Create successful')
    if request.method == 'POST' and 'editHouse' in request.POST:
        if House.objects.filter(id=request.POST.get('id')).count() == 0:
            messages.warning(request, 'Given House ID doesn\'t exist')
            return HttpResponseRedirect(reverse("houses"))
        newAddress = request.POST.get('address')
        if newAddress == '':
            newAddress = House.objects.filter(id=request.POST.get('id'))[0].address
        newHT = request.POST.get('houseType')
        if newHT == '':
            newHT = House.objects.filter(id=request.POST.get('id'))[0].houseType
        House.objects.filter(id=request.POST.get('id')).update(address=newAddress,
                                                                   houseType=newHT)
        messages.success(request, 'Edit successful')
    if request.method == 'POST' and 'deleteHouse' in request.POST:
        House.objects.filter(id=request.POST.get('id')).delete()
        messages.success(request, 'Delete successful')
    return render(request, 'houses.html', {'data': House.objects.all(),
                                           'mode': mode})


def login(request):
    if request.method == 'POST' and 'login' in request.POST:
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Successfully logged in')
            return HttpResponseRedirect(reverse("persons"))
        else:
            messages.error(request, 'Wrong login credentials')
            return HttpResponseRedirect(reverse("login"))
    return render(request, 'login.html', {})


def register(request):
    if request.method == 'POST' and 'register' in request.POST:
        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, 'Username already taken')
            return HttpResponseRedirect(reverse("register"))
        if request.POST.get('username') == '' or\
                request.POST.get('password1') == '' or\
                request.POST.get('password2') == '' or\
                request.POST.get('email') == '':
            messages.warning(request, 'Leave no fields empty')
            return HttpResponseRedirect(reverse("register"))
        if request.POST.get('password1') != request.POST.get('password2'):
            messages.warning(request, 'Passwords must match')
            return HttpResponseRedirect(reverse("register"))
        user = User.objects.create_user(request.POST.get('username'),
                                        request.POST.get('email'),
                                        request.POST.get('password1'))
        user.save()
        messages.success(request, 'Successful registration')
    return render(request, 'register.html', {})


def logout(request):
    auth_logout(request)
    messages.success(request, 'Successfully logged out')
    return HttpResponseRedirect(reverse("login"))
