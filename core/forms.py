from django import forms
from core.models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        # widgets = {
        #     'name' : forms.TextInput(attrs={'class':'form-control'}),
        #     'category': forms.Select(attrs={'class':'form-control'}),
        #     'desc': forms.Textarea(attrs={'class':'form-control'}),
        #     'price': forms.NumberInput(attrs={'class':'form-control'}),
        #     'product_available_cnt': forms.NumberInput(attrs={'class':'form-control'}),
        #     'img': forms.FileInput(attrs={'class':'form-control'}),
        # }

        labels = {
            "desc" : "Description",
            "product_available_cnt": "Product Available Count",
            "img" : "Image"
            
        }

class CheckoutForm(forms.Form):
    address = forms.CharField(label='Address',widget=forms.TextInput(attrs={'placeholder': '1234 Main St'}))
    address2 = forms.CharField(required=False,label='Address (Optional)',widget=forms.TextInput(attrs={'placeholder': '1234 Main St'}))
    phone_no = forms.CharField(label='Phone No',widget=forms.TextInput(attrs={'placeholder': '9012345678'}))
    state = forms.CharField(label='State',widget=forms.TextInput(attrs={'placeholder': 'Enter your State'}))
    zipcode = forms.CharField(label='Zip code',widget=forms.TextInput(attrs={'placeholder': 'Enter your zipcode'}))