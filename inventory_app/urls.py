from django.urls import path, include
from . import views
from rest_framework import routers
from .views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

app_name = 'inventory_app'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('new/', views.product_create, name='product_create'),
    path('bill/', views.bill_create, name='bill_create'),
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/<int:pk>/', views.bill_detail, name='bill_detail'),
    path('bills/<int:pk>/pdf/', views.bill_pdf, name='bill_pdf'),
    path('api/', include(router.urls)),
]
