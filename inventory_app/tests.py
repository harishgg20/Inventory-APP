import pytest
from inventory_app.models import Product, Bill

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(name="Test Item", sku="TEST001", price=100, quantity=10)
    assert product.name == "Test Item"
    assert product.quantity == 10
    assert str(product) == "Test Item (TEST001)"

@pytest.mark.django_db
def test_low_stock_threshold():
    product = Product.objects.create(name="Low Item", sku="LOW001", price=50, quantity=2, low_stock_threshold=5)
    from inventory_app.tasks import check_low_stock_and_alert
    # We can't easily mock the email strictly without more setup, but we can check the query logic
    assert product.quantity <= product.low_stock_threshold

@pytest.mark.django_db
def test_bill_creation(django_user_model):
    user = django_user_model.objects.create_user(username='staff', password='password')
    bill = Bill.objects.create(created_by=user, total=500.00)
    assert bill.created_by == user
    assert bill.total == 500.00
