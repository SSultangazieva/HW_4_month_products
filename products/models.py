from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hashtag(models.Model):
    title = models.CharField(max_length=250)

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField()

class Products(models.Model): # класс Python, который наследуется о модуля- django.db.models.Model.
    # Каждый атрибут модели - ПОЛЕ БД
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)#у 1пользователя много постов
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag)

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #у 1пользователя много комментариев
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    Creted_Date = models.DateField(auto_now_add=True)
