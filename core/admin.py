from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'current_stock', 'sale_price', 'is_active', 'popularity_score')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'code')
    list_editable = ('is_active',)

admin.site.register(ProductFormula)
admin.site.register(RawMaterial)
admin.site.register(Purchase)
admin.site.register(Production)
admin.site.register(StockMovement)
admin.site.register(Sale)
