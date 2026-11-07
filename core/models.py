from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    code = models.CharField(max_length=50, unique=True, verbose_name='کد محصول')
    category = models.CharField(max_length=100, blank=True, verbose_name='دسته‌بندی')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='قیمت فروش')
    production_cost = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='هزینه تولید تقریبی')
    min_stock = models.PositiveIntegerField(default=0, verbose_name='حداقل موجودی')
    current_stock = models.IntegerField(default=0, verbose_name='موجودی فعلی')
    popularity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='امتیاز محبوبیت')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def profit_margin(self):
        if self.sale_price > 0:
            return ((self.sale_price - self.production_cost) / self.sale_price) * 100
        return 0

    @property
    def is_low_stock(self):
        return self.current_stock <= self.min_stock

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

class RawMaterial(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام ماده اولیه')
    code = models.CharField(max_length=50, unique=True, verbose_name='کد')
    unit = models.CharField(max_length=30, default='کیلوگرم', verbose_name='واحد')
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='موجودی فعلی')
    min_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='حداقل موجودی')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ماده اولیه'
        verbose_name_plural = 'مواد اولیه'

    def __str__(self):
        return self.name

class Purchase(models.Model):
    COUNTRY_CHOICES = [
        ('RU', 'روسیه'),
        ('EU', 'اروپا'),
        ('IR', 'ایران'),
        ('OTHER', 'سایر'),
    ]
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, related_name='purchases', verbose_name='ماده اولیه')
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, verbose_name='کشور مبدأ')
    supplier = models.CharField(max_length=200, blank=True, verbose_name='تأمین‌کننده')
    purchase_date = models.DateField(verbose_name='تاریخ خرید')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='مقدار')
    unit_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت واحد')
    currency = models.CharField(max_length=10, default='IRR', verbose_name='ارز')
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='هزینه حمل')
    extra_cost = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='هزینه‌های جانبی')
    total_cost = models.DecimalField(max_digits=14, decimal_places=0, default=0, verbose_name='قیمت تمام‌شده')
    reference_code = models.CharField(max_length=100, blank=True, verbose_name='شماره خرید')
    notes = models.TextField(blank=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'خرید ماده اولیه'
        verbose_name_plural = 'خریدهای مواد اولیه'
        ordering = ['-purchase_date']

    def save(self, *args, **kwargs):
        self.total_cost = (self.quantity * self.unit_price) + self.shipping_cost + self.extra_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.raw_material.name} - {self.purchase_date}"

class Production(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productions', verbose_name='محصول')
    formula = models.ForeignKey(ProductFormula, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='فرمول')
    production_date = models.DateField(verbose_name='تاریخ تولید')
    batch_number = models.CharField(max_length=100, verbose_name='شماره بچ')
    quantity = models.PositiveIntegerField(verbose_name='مقدار تولید')
    waste_quantity = models.PositiveIntegerField(default=0, verbose_name='ضایعات')
    notes = models.TextField(blank=True, verbose_name='توضیحات')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تولید'
        verbose_name_plural = 'تولیدات'
        ordering = ['-production_date']

    def __str__(self):
        return f"{self.product.name} - {self.batch_number}"

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'ورود'),
        ('OUT', 'خروج'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='stock_movements')
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, null=True, blank=True, related_name='stock_movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES, verbose_name='نوع')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='مقدار')
    date = models.DateField(verbose_name='تاریخ')
    reason = models.CharField(max_length=255, blank=True, verbose_name='علت')
    notes = models.TextField(blank=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'گردش موجودی'
        verbose_name_plural = 'گردش‌های موجودی'
        ordering = ['-date']

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales', verbose_name='محصول')
    sale_date = models.DateField(verbose_name='تاریخ فروش')
    quantity = models.PositiveIntegerField(verbose_name='مقدار')
    unit_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت واحد')
    total_amount = models.DecimalField(max_digits=14, decimal_places=0, verbose_name='مبلغ کل')
    notes = models.TextField(blank=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فروش'
        verbose_name_plural = 'فروش‌ها'
        ordering = ['-sale_date']

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.sale_date}"
