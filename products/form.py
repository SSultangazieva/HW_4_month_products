from django import forms


class ProductCreateForm(forms.Form):
    name = forms.CharField(min_length=2)
    description = forms.CharField(widget=forms.Textarea())
    price = forms.FloatField(required=False)



class ReviewCreateForm(forms.Form):
    text = forms.CharField()

