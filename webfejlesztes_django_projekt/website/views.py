from django.shortcuts import render


def home(request):
    return render(request, 'index.html', {})


def persons(request):
    return render(request, 'persons.html', {})


def houses(request):
    return render(request, 'houses.html', {})
