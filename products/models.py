from django.db import models

# Create your models here.
class Products(models.Model): # класс Python, который наследуется о модуля- django.db.models.Model.
    # Каждый атрибут модели - ПОЛЕ БД
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

