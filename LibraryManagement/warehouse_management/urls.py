from django.urls import path

from .views import *

urlpatterns = [
    path('',login),

    path('getProduct/?page=<str:page>',getAllProducts),
    path('getProduct/',getAllProducts),
    path('editProduct/<str:product_id>/',editProduct),
    path('addProduct/',addProduct),
    path('addncc/',addNCC),
    path('addcustomer/',addCustomer),
    path('customer/',getCustomer),
    path('customer/<str:customer_code>/',getCustomer),
    path('nhacungcap/',getNCC),
    path('nhacungcap/<str:ncc_id>/',getNCC),
    path('addphieuxuat/',addPhieuXuat),
    path('updateproduct/',updateProduct),
    path('home_manager/',home_manager),
    path('export-excel/',export_products_excel),
    path('forgot/',forgot),
    path('verify_otp/',verify_otp),
    path('updatepassword/',updatepassword),
    path('deleteProduct/',updatepassword),
    path('deleteProduct/<str:product_code>/', delete_product),
    path('filter/', filter_products),
]
