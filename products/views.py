from django.shortcuts import render
from products.models import *


# Create your views here.
# логика отдачи главной страницы:
def main(request):
    if request.method == 'GET':
        #1-поступивший запрос 2-что мы отрисовываем (т.е. html файл)
        return render(request, 'layouts/index.html')


def cat_views(request):
    if request.method == 'GET':
        # достать все посты в БД, через объектный менеджер objects (он позв работать с БД)
        cat = Category.objects.all()

        # отправить все посты на наш шаблон
        context = {
            'cat': cat
        }
        return render(request, 'categories/index.html', context=context)
        # параметр context= чтобы из view отправить данные


def cat_detail_view(request, id):
    if request.method == 'GET':
        cat_obj = Category.objects.get(id=id)
        products = Products.objects.filter(category=cat_obj)
        context = {
            'cat_key': cat_obj,
            'products_key': products
        }
        return render(request, 'categories/detail.html', context=context)


def products_views(request):
    if request.method == 'GET':
        # достать все посты в БД, через объектный менеджер objects (он позв работать с БД)
        products_1 = Products.objects.all()

        # отправить все посты на наш шаблон
        context = {
            'products': products_1
        }
        return render(request, 'products/products.html', context=context)
        # параметр context= чтобы из view отправить данные


def pruduct_detail_view(request, id):
    if request.method == 'GET':
        product_obj = Products.objects.get(id=id)
        review = Review.objects.filter(product=product_obj)
        context = {
            'product_key': product_obj,
            'comment_key': review
        }
        return render(request, 'products/detail.html', context=context)
