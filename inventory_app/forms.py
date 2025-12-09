from django import forms
from .models import Product, Bill, BillItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','sku','description','price','quantity','low_stock_threshold']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['created_by']
