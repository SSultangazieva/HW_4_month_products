from django.shortcuts import render, redirect
from products.models import Products, Category, Review
from products.form import ProductCreateForm, ReviewCreateForm
from django.views.generic import ListView, CreateView, DetailView, FormView

# лимит объектов на одной странице для пагинации:
PAGINATION_LIMIT = 3


# Create your views here.
# логика отдачи главной страницы:
# def main(request):
#     if request.method == 'GET':
#         #1-поступивший запрос 2-что мы отрисовываем (т.е. html файл)
#         return render(request, 'layouts/index.html')

class MainView(ListView):
    model = Products
    template_name = 'layouts/index.html'


# def cat_views(request):
#     if request.method == 'GET':
#         # достать все посты в БД, через объектный менеджер objects (он позв работать с БД)
#         cat = Category.objects.all()
#
#         # отправить все посты на наш шаблон
#         context = {
#             'cat': cat
#         }
#         return render(request, 'categories/index.html', context=context)
#         # параметр context= чтобы из view отправить данные

class CategoriesCBV(ListView):
    queryset = Category.objects.all()
    template_name = 'categories/index.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name, context={
            'cat': Category.objects.all(),
        })

def cat_detail_view(request, id):
    if request.method == 'GET':
        cat_obj = Category.objects.get(id=id)
        products = Products.objects.filter(category=cat_obj)
        context = {
            'cat_key': cat_obj,
            'products_key': products
        }
        return render(request, 'categories/detail.html', context=context)


# def products_views(request):
#     if request.method == 'GET':
#         # достать все посты в БД, через объектный менеджер objects (он позв работать с БД)
#         products_1 = Products.objects.all()
#         # достать сам запрос:
#         search = request.GET.get('search')
#         # достать страницу из query запроса, по дефолту 1 страница
#         page = int(request.GET.get('page', 1))
#         if search is not None:
#             # найти продукты согласно запросу и присвоить его переменной.Важно правильно указать параметр
#             products_1 = Products.objects.filter(name__icontains=search) or \
#                          Products.objects.filter(description__icontains=search)
#         max_page = products_1.__len__() / PAGINATION_LIMIT
#         if round(max_page) < max_page:# для чисел с плавающей точкой ДО 0,5 чтобы прибавить к ним 1
#             max_page = round(max_page) + 1
#         else:  # для чисел ПОСЛЕ 0,5
#             max_page = round(max_page)
#         # срез продуктов для каждой страницы (с какого по какой пост отрисовать):
#         products_1 = products_1[PAGINATION_LIMIT * (page-1): PAGINATION_LIMIT * page]
#
#         # отправить все посты на наш шаблон
#         context = {
#             'products': products_1,
#             'autor': request.user,
#             'max_page': range(1, max_page+1),
#             'user': request.user
#         }
#         return render(request, 'products/products.html', context=context)
#         # параметр context= чтобы из view отправить данные
#

class Products_View(ListView):
    model = Products
    template_name = 'products/products.html'

    def get(self, request, **kwargs):
        products_1 = self.get_queryset()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search is not None:
            products_1 = Products.objects.filter(name__icontains=search) or \
                         Products.objects.filter(description__icontains=search)
        max_page = products_1.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        products_1 = products_1[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]

        context = {
            'products': products_1,
            'autor': request.user,
            'max_page': range(1, max_page + 1),
            'user': request.user
        }
        return render(request, self.template_name, context=context)


def pruduct_detail_view(request, id):
    form = ReviewCreateForm(data=request.POST)
    if request.method == 'GET':
        product_obj = Products.objects.get(id=id)
        review = Review.objects.filter(product=product_obj)
        context = {
            'product_key': product_obj,
            'comment_key': review,
            'comment_form': ReviewCreateForm,
            'user': request.user
        }
        return render(request, 'products/detail.html', context=context)

    elif request.method == 'POST':
        if form.is_valid():
            Review.objects.create(
                author=request.user,
                text=form.cleaned_data.get('text'),
                product_id=id
            )
            return redirect(f"/products/{id}/")
#
# def check_user(request):
#     return None if request.user.is_anonymous else request.user
# def rend(request):
#     if request.method == 'GET':
#         return render(request, 'layouts/index.html', context={
#             "user": check_user(request)
#         })
#
# class Products_Detail(DetailView, CreateView):
#     queryset = Products.objects.all()
#     context_object_name = "product_key"
#     template_name = "products/detail.html"
#     form_class = ReviewCreateForm
#     model = Products
#
#
#     def get(self, request, pk=None, **kwargs):
#         product = Products.objects.get(pk=pk)
#         return render(request, self.template_name, context={
#             "comment_form": self.form_class,
#             "product_key": product,
#             'comment_key': product.reviews.all(),
#             "categories": product.category
#         })
#
#     def post(self, request, pk=None, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             Review.objects.create(
#                 product_id=pk,
#                 author_id=request.user.id,
#                 text=form.cleaned_data.get("text")
#             )
#             return redirect(f"/products/{pk}/")



def create_products_view(request):
    if request.method == 'GET' and not request.user.is_anonymous:
        context = {
            'form': ProductCreateForm
        }
        return render(request, 'products/create.html', context=context)
    elif request.user.is_anonymous:
        return redirect('/products')

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

#
# class ProductCreateCBV(FormView):
#     model = Products
#     template_name = 'products/create.html'
#     form_class = ProductCreateForm
#     queryset = Products.objects.all()
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         return {
#             'form': kwargs['form'] if kwargs.get('form') else self.form_class
#             }
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(data=request.POST)
#
#         if form.is_valid():
#             self.model.objects.create(
#                 author_id=request.user.id,
#                 title=form.cleaned_data.get('title'),
#                 description=form.cleaned_data.get('description'),
#                 price=form.cleaned_data.get('price'),
#
#             )
#             return redirect('/products')
#         else:
#             return render(request, self.template_name, context=self.get_context_data(form=form))
