from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('persons', views.persons, name="persons"),
    path('houses', views.houses, name="houses"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
]
