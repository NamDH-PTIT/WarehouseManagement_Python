from django.urls import path
from .views import *

urlpatterns = [
    path('',home_staff),
    path('getProduct/',getAllProducts),
    path('editProduct/<str:product_id>/',editProduct),
    path('addProduct/',addProduct),
    path('addncc/',addNCC),
    path('addcustomer/',addCustomer),
    path('customer/',getCustomer),
    path('customer/<str:customer_id>/',getCustomer),
    path('nhacungcap/',getNCC),
    path('nhacungcap/<str:ncc_id>/',getNCC),
    path('addphieuxuat/',addPhieuNhap),
    path('updateproduct/',updateProduct),
    path('home_manager/',home_manager),
    path('export_products/',export_products_excel),
]
