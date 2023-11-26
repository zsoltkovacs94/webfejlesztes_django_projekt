from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('persons', views.persons, name="persons"),
    path('houses', views.houses, name="houses"),
    path('addTestPerson', views.addTestPerson, name="addTestPerson"),
    path('addTestHouse', views.addTestHouse, name="addTestHouse"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
]
