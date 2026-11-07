from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    code = models.CharField(max_length=50, unique=True, verbose_name='کد محصول')
    category = models.CharField(max_length=100, blank=True, verbose_name='دسته‌بندی')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"


class ProductFormula(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='formulas', verbose_name='محصول')
    version = models.CharField(max_length=50, verbose_name='نسخه فرمول')
    description = models.TextField(blank=True, verbose_name='توضیحات فرمول')
    is_current = models.BooleanField(default=False, verbose_name='فرمول فعلی')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فرمول محصول'
        verbose_name_plural = 'فرمول‌های محصول'

    def __str__(self):
        return f"{self.product.name} - {self.version}"
