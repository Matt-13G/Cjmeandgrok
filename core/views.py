from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product, Sale

@login_required
def dashboard(request):
    products = Product.objects.all()[:10]
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    low_stock_count = Product.objects.filter(current_stock__lte=models.F('min_stock')).count()
    
    today = timezone.now().date()
    today_sales = Sale.objects.filter(sale_date=today).count()

    context = {
        'products': products,
        'total_products': total_products,
        'active_products': active_products,
        'low_stock_count': low_stock_count,
        'today_sales': today_sales,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/product_detail.html', {'product': product})
