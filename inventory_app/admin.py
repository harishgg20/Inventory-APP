from django.contrib import admin
from .models import Product, Bill, BillItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','sku','price','quantity','low_stock_threshold')
    search_fields = ('name','sku')

class BillItemInline(admin.TabularInline):
    model = BillItem

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = [BillItemInline]
    list_display = ('id','created_by','created_at','total')
