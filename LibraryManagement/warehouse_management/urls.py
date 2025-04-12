from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
                  path('', login),

                  path('getProduct/?page=<str:page>', getAllProducts),
                  path('getProduct/', getAllProducts),
                  path('editProduct/<str:product_id>/', editProduct),
                  path('addphieunhap/', addPhieuNhap),
                  path('addncc/', addNCC),
                  path('addcustomer/', addCustomer),
                  path('customer/', getCustomer),
                  path('customer/<str:customer_code>/', getCustomer),
                  path('nhacungcap/', getNCC),
                  path('nhacungcap/<str:ncc_id>/', getNCC),
                  path('addphieuxuat/', addPhieuXuat),
                  path('updateproduct/', updateProduct),
                  path('home_manager/', home_manager),
                  path('export-excel/', export_products_excel),
                  path('forgot/', forgot),
                  path('verify_otp/', verify_otp),
                  path('updatepassword/', updatepassword),
                  path('deleteProduct/', updatepassword),
                  path('deleteProduct/<str:product_code>/', delete_product),
                  path('filter/', filter_products),
                  path('getuser/', getuser),
                  path('adduser/', adduser),
                  path('getuser/user_filter', user_filter),
                  path('user_excel/', export_user),
                  path('getuser/edituser/id=<str:userid>', getuserbyid),
                  path('updateuser/', updateuser),
                  path('getuser/userdelete/id=<str:userid>', deleteuser),
                  path('addproduct/', addproduct),
                  path('warehouse_management/', warehouse_managment),
                  path('export/', exportkho),
                  path('chuyenkho/productCode=<str:productCode>', chuyenkho),
                  path('chuyenkho/', chuyensp),
                  path('quanlynhaphang/', quanlynhaphang),
                  path('quanlykhachhang', quanlykhachhang)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
