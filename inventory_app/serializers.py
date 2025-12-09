from rest_framework import serializers
from .models import Product, Bill, BillItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = ['product','quantity','price']

class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True)
    class Meta:
        model = Bill
        fields = ['id','created_by','created_at','total','items']
