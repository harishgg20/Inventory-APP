from django.db import transaction
from .models import Product
from .tasks import async_generate_bill

def finalize_bill(bill, user):
    """
    Finalizes a bill: duplicates stock check with locking, decrements stock,
    and triggers async PDF/email generation.
    """
    with transaction.atomic():
        # Iterate over items. To ensure inventory safety, we should lock the Product rows.
        # The original snippet locked bill.items (select_for_update), which locks the BillItem rows.
        # To strictly prevent race conditions on Product quantity, we lock the Products here.
        
        for item in bill.items.all():
            # Lock the product row for update to prevent concurrent decrements miscounting
            # SQLite doesn't support select_for_update well (locks entire DB), so we skip it there.
            from django.db import connection
            if connection.vendor == 'sqlite':
                p = Product.objects.get(pk=item.product.pk)
            else:
                p = Product.objects.select_for_update().get(pk=item.product.pk)
            
            if p.quantity < item.quantity:
                raise ValueError(f'Insufficient stock for {p.sku} (Requested: {item.quantity}, Available: {p.quantity})')
            
            p.quantity -= item.quantity
            p.save()
            
    # Trigger async task after transaction commits
    async_generate_bill.delay(bill.id)
