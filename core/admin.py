from django.contrib import admin
from .models import Product, ProductFormula

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'code')

@admin.register(ProductFormula)
class ProductFormulaAdmin(admin.ModelAdmin):
    list_display = ('product', 'version', 'is_current', 'created_at')
    list_filter = ('is_current',)
