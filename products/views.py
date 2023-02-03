from django.shortcuts import render, redirect
from products.models import Products, Category, Review
from products.form import ProductCreateForm, ReviewCreateForm

# лимит объектов на одной странице для пагинации:
PAGINATION_LIMIT = 3


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
        # достать сам запрос:
        search = request.GET.get('search')
        # достать страницу из query запроса, по дефолту 1 страница
        page = int(request.GET.get('page', 1))
        if search is not None:
            # найти продукты согласно запросу и присвоить его переменной.Важно правильно указать параметр
            products_1 = Products.objects.filter(name__icontains=search)
        max_page = products_1.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:# для чисел с плавающей точкой ДО 0,5 чтобы прибавить к ним 1
            max_page = round(max_page) + 1
        else:  # для чисел ПОСЛЕ 0,5
            max_page = round(max_page)
        # срез продуктов для каждой страницы (с какого по какой пост отрисовать):
        products_1 = products_1[PAGINATION_LIMIT * (page-1): PAGINATION_LIMIT * page]
        # отправить все посты на наш шаблон
        context = {
            'products': products_1,
            'max_page': range(1, max_page+1) }
        return render(request, 'products/products.html', context=context)
        # параметр context= чтобы из view отправить данные


def pruduct_detail_view(request, id):
    form = ReviewCreateForm(data=request.POST)
    if request.method == 'GET':
        product_obj = Products.objects.get(id=id)
        review = Review.objects.filter(product=product_obj)
        context = {
            'product_key': product_obj,
            'comment_key': review,
            'comment_form': ReviewCreateForm
        }
        return render(request, 'products/detail.html', context=context)

    elif request.method == 'POST':
        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                product_id=id
            )
            return redirect(f"/products/{id}/")


def crate_products_view(request):
    if request.method == 'GET':
        context = {
            'form': ProductCreateForm
        }
        return render(request, 'products/create.html', context=context)

    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Products.objects.create(
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data['price'] if form.cleaned_data['price'] is not None else 5
            )
            return redirect('/products/')
        return render(request, 'products/create.html', context={
            'form': form
        })

