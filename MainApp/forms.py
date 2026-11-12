from django import forms
from .models import Products, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__' 

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['products']
        widgets = {
            'products': forms.CheckboxSelectMultiple(),
        }
