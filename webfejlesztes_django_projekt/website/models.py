from django.db import models


class House(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100, unique=True)
    houseType = models.CharField(max_length=20)


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    birth = models.DateField()
