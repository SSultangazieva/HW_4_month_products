from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField()
# Create your models here.
class Products(models.Model): # класс Python, который наследуется о модуля- django.db.models.Model.
    # Каждый атрибут модели - ПОЛЕ БД
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255, default=None)
    description = models.TextField()
    price = models.FloatField()
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, blank=True)

class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    text = models.TextField()
    Creted_Date = models.DateField(auto_now_add=True)
