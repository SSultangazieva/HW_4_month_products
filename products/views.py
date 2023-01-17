from django.shortcuts import render
from products.models import Products

# Create your views here.
# логика отдачи главной страницы:
def main(request):
    if request.method == 'GET':
        #1-поступивший запрос 2-что мы отрисовываем (т.е. html файл)
        return render(request, 'layouts/index.html')

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
