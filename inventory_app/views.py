from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import JsonResponse
from .models import Product, Bill, BillItem
from .forms import ProductForm, BillForm
from .services import finalize_bill
from rest_framework import viewsets
from .serializers import ProductSerializer, BillSerializer

from django.db.models import Sum, F

from django.db.models import Sum, F, Q

@login_required
def dashboard(request):
    """
    Main Home View: Shows Stats and potentially Charts
    """
    products = Product.objects.all()
    # Stats
    total_products = products.count()
    low_stock_count = products.filter(quantity__lte=F('low_stock_threshold')).count()
    total_value = products.aggregate(val=Sum(F('price') * F('quantity')))['val'] or 0
    
    # Recent Bills
    recent_bills = Bill.objects.order_by('-created_at')[:5]

    # Chart Data (Top 5 Products by Stock)
    top_products = products.order_by('-quantity')[:5]
    chart_labels = [p.name for p in top_products]
    chart_stock = [p.quantity for p in top_products]
    chart_value = [float(p.price * p.quantity) for p in top_products]
    
    context = {
        'recent_bills': recent_bills,
        'chart_labels': json.dumps(chart_labels),
        'chart_stock': json.dumps(chart_stock),
        'chart_value': json.dumps(chart_value),
        # Default stats visible to all staff
        'stats': {
            'total_products': total_products,
            'low_stock': low_stock_count,
            'total_value': 0 # Hidden by default
        }
    }

    # Hide Financials for non-superusers
    if request.user.is_superuser:
        context['stats']['total_value'] = total_value
        context['is_admin'] = True
    else:
        context['is_admin'] = False
    return render(request, 'inventory_app/dashboard.html', context)

@login_required
def product_list(request):
    """
    Product Management View with Search
    """
    query = request.GET.get('q', '')
    products = Product.objects.all().order_by('name')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(sku__icontains=query)
        )
    
    return render(request, 'inventory_app/product_list.html', {'products': products, 'search_query': query})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_app:product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory_app/product_form.html', {'form': form})

import json

@login_required
def bill_create(request):
    if request.method == 'POST':
        try:
            # Handle JSON data (POS style)
            data = json.loads(request.body)
            items = data.get('items', [])
            
            if not items:
                return JsonResponse({'error': 'No items in bill'}, status=400)

            if not items:
                return JsonResponse({'error': 'No items in bill'}, status=400)

            with transaction.atomic():
                email = data.get('customer_email', '')
                bill = Bill.objects.create(created_by=request.user, customer_email=email)
                
                for item in items:
                    product_id = item.get('id')
                    try:
                        qty = int(item.get('qty'))
                    except (ValueError, TypeError):
                        raise ValueError(f"Invalid quantity for product {product_id}")

                    if qty <= 0:
                        continue

                    product = Product.objects.get(pk=product_id)
                    BillItem.objects.create(bill=bill, product=product, quantity=qty, price=product.price)
                
                # Finalize (deduct stock, etc)
                finalize_bill(bill, request.user)
            
            return JsonResponse({'success': True, 'bill_id': bill.id})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"Server Error: {str(e)}"}, status=500)

    products = Product.objects.all()
    # Serialize products for JS
    products_json = json.dumps([
        {'id': p.id, 'name': p.name, 'sku': p.sku, 'price': float(p.price), 'stock': p.quantity}
        for p in products
    ])
    return render(request, 'inventory_app/bill_create.html', {'products': products, 'products_json': products_json})

@login_required
def bill_list(request):
    bills = Bill.objects.all().order_by('-created_at')
    return render(request, 'inventory_app/bill_list.html', {'bills': bills})

@login_required
def bill_detail(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    return render(request, 'inventory_app/bill_detail.html', {'bill': bill})

from .utils import render_to_pdf

@login_required
def bill_pdf(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    pdf = render_to_pdf('inventory_app/bill_detail.html', {'bill': bill})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
