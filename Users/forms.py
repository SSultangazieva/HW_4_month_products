from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput()) #widget чтобы скрыть ввод пороля

class RegsiterForm(forms.Form):
    username = forms.CharField()
    password_1 = forms.CharField(widget=forms.PasswordInput()) #Запросить
    password_2 = forms.CharField(widget=forms.PasswordInput()) #Подтвердить



