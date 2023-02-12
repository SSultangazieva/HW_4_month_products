from django.shortcuts import render, redirect
from Users.forms import LoginForm, RegsiterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, RedirectView


# Create your views here.
#
# class LoginView(ListView, CreateView):
#     template_name = 'users/login.html'
#
#     def get(self, request, **kwargs):
#         context = {
#             'form': LoginForm,
#         }
#         return render(request, self.template_name, context=context)
#
#     def post(self, request, **kwargs):
#         form = LoginForm(data=request.POST)
#
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data.get('username'),
#                 password=form.cleaned_data.get('password')
#             )
#             if user:
#                 login(request, user)
#                 return redirect('/products/')
#             else:
#                 form.add_error('username', 'Еще раз пробуй, не сдавайся, позорься до конца!')
#
#         return render(request, 'users/login.html', context={
#             'form': form,
#         })
#
#
# class LogoutView(RedirectView):
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('/products/')
#
#
# class RegisterView(ListView, CreateView):
#     template_name = 'users/register.html'
#
#     def get(self, request, **kwargs):
#         context = {
#             'form': RegsiterForm,
#         }
#         return render(request, 'users/register.html', context=context)
#
#     def post(self, request, *args, **kwargs):
#         form = RegsiterForm(data=request.POST)
#
#         if form.is_valid():
#             password_1, password_2 = form.cleaned_data.get('password1'), form.cleaned_data.get('password2')
#             if password_1 == password_2:
#                 User.objects.create_user(
#                     username=form.cleaned_data.get('username'),
#                     password=form.cleaned_data.get('password_1')
#                 )
#                 return redirect('/users/login/')
#             else:
#                 form.add_error('password_1', 'не тупи')
#
#         return render(request, 'users/register.html', context={
#             'form': form,
#         })




def auth_view(request):
    # если это get запрос нужно отрисовать формочку с шаблоном:
    if request.method == 'GET':
        context = {
            'form': LoginForm
        }
        # в контексте отрисовать форму
        return render(request, 'users/auth.html', context=context)

    if request.method == 'POST':
        data = request.POST
        # данные отправляем в формочку чтобы работать с этой информацией
        # у форм есть атрибут data=  метод is_valid будет работ с данными переданнми data=
        form = LoginForm(data=data)

        # аутентифицировать пользователя если данные проходят валидность
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            # print(user) admin
            # а если отправить неверный логин или пароль, то будет None, т.к. такого польз нет

            # после успешной аутентификации, нужно АВТОРИЗОВАТЬСЯ
            # если юзер есть:
            if user:
                login(request, user)
                return redirect('/products')
            # если не успешно, отрисовать страницу, но без подсказок (brute force)
            else:
                form.add_error('username', 'Еще раз пробуй, не сдавайся, позорься до конца!')

        # если никакая проверка не стработала выведем ту же станицу
        return render(request, 'users/auth.html', context={
            "form": form
        })


def logout_view(request):
    logout(request)
    return redirect('/products/')


def register_view(request):
    if request.method == 'GET':
        context = {
            "form": RegsiterForm
        }
        return render(request, 'users/register.html', context=context)

    if request.method == 'POST':
        form = RegsiterForm(data=request.POST)

        if form.is_valid():
            password_1,password_2 = form.cleaned_data.get('password_1'),form.cleaned_data.get('password_2')
            if password_1 == password_2:
                # только в этом случае будем создавать пользователя:
                User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password_1')
                )
                return redirect('/users/login/')
            else:
                form.add_error('password_1', 'не тупи')

        return render(request, 'users/register.html', context={
            'form':form
        })
