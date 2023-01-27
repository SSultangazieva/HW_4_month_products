from django import forms


class ProductCreateForm(forms.Form):
    title = forms.CharField(min_length=2)
    description = forms.CharField(widget=forms.Textarea())
    price = forms.FloatField(min_value=1)


class ReviewCreateForm(forms.Form):
    text = forms.CharField()

