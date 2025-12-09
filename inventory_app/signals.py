from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import check_low_stock_and_alert

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    if instance.quantity <= instance.low_stock_threshold:
        # schedule background alert (debounced by Celery rate limits)
        check_low_stock_and_alert.delay()
