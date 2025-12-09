from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Bill

@shared_task
def check_low_stock_and_alert():
    from django.db.models import F
    
    # Find products where quantity <= threshold
    low = Product.objects.filter(quantity__lte=F('low_stock_threshold'))
    
    if not low.exists():
        return 'no low stock'
        
    body_lines = ["The following items are low in stock:", ""]
    for p in low:
        body_lines.append(f"- {p.name} (SKU: {p.sku}): {p.quantity} remaining")
        
    send_mail(
        'Low Stock Alert - Inventory System',
        '\n'.join(body_lines),
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER], # Sending to self/admin
        fail_silently=False,
    )
    return f'sent {low.count()} alerts'

@shared_task
def async_generate_bill(bill_id):
    # small example: fetch bill, compute totals, and optionally email invoice
    # The snippet had `from .models import Bill` inside function, keeping it.
    from .models import Bill
    bill = Bill.objects.get(pk=bill_id)
    total = 0
    for item in bill.items.all():
        total += item.quantity * float(item.price)
    bill.total = total
    bill.save()
    
    # Send Email Receipt
    if bill.customer_email:
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f"Receipt for Bill #{bill.id}"
        message = f"Thank you for shopping!\n\nTotal Amount: {total}\n\nHave a great day!"
        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST_USER, 
            [bill.customer_email], 
            fail_silently=True
        )

    return f'bill {bill_id} updated'
