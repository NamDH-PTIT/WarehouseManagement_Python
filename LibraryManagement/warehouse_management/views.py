import json

import openpyxl
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from database.models import *
from warehouse_management.response.ApiResponse import ApiResponse



# Create your views here.
@require_http_methods(["GET"])
@csrf_exempt
def home_staff(request):
    # return ApiResponse(message="Dữ liệu lấy thành công", data={"id": 1, "name": "Sản phẩm A"}).to_json()
    return render(request,'LibraryManagement/index.html')

@require_http_methods(["GET"])
@csrf_exempt
def getAllProducts(request):
    products = list(Product.objects.raw("select * from database_product order by quantity asc"))
    return render(request,'LibraryManagement/home.html',{"products":products})
@require_http_methods(["GET"])
@csrf_exempt
def editProduct(request,product_id):
    product = get_object_or_404(Product.objects.values(), code=product_id)  # Tìm sản phẩm theo code, nếu không có thì trả về 404
    return ApiResponse(message="oke",data={"product":product}).to_json()
@require_http_methods(["POST"])
@csrf_exempt
def addProduct(request):
    data = json.loads(request.body)
    try:
        with transaction.atomic():
            nccRequest=data.get("nameNCC")
            ncc=NhaCungCap.objects.get(nameNCC=nccRequest)
            phieuNhapRequest=data.get("phieuNhap")
            phieuNhap=PhieuNhap.objects.create(
                date=phieuNhapRequest.get("date"),
                totalPrice=phieuNhapRequest.get("totalPrice"),
                notes=phieuNhapRequest.get("notes"),
                codeNCC=ncc
            )
            chiTietPhieuNhapRequest=data.get("chiTietPhieuNhap")
            for item in chiTietPhieuNhapRequest:
                if(Product.objects.filter(code=item["code"]).exists()):
                    product=Product.objects.get(code=item["code"])
                    product.quantity+=item["quantity"]
                    product.save()
                else:
                    product =Product.objects.create(
                        code=item.get("code"),
                        nameProduct=item.get("nameProduct"),
                        category=item.get("category"),
                        quantity=item.get("quantity"),
                        importPrice=item.get("importPrice"),
                    )
                ChiTietPhieuNhap.objects.create(
                    codeProduct=product,
                    codePhieuNhap=phieuNhap,
                    quantity=item.get("quantity"),
                    importPrice=item.get("importPrice"),
                )
            return ApiResponse(message="thêm phiếu nhập thành công").to_json()
    except Exception as e:
        return ApiResponse(message="thêm phiếu nhập Không thành công",status="false").to_json()
@csrf_exempt
@require_http_methods(["POST"])
def addNCC(request):
    data = json.loads(request.body)
    nccRequest=data.get("nccInfo")
    if NhaCungCap.objects.filter(nameNCC=nccRequest.get("nameNCC")).exists():
        nccResponse=NhaCungCap.objects.get(nameNCC=nccRequest.get("nameNCC"))
        return JsonResponse({"message": "Nhà cung cấp đã tồn tại!", "model": model_to_dict(nccResponse)}, status=400)
    ncc=NhaCungCap.objects.create(
        nameNCC=nccRequest.get("nameNCC"),
        addressNCC=nccRequest.get("addressNCC"),
        code=nccRequest.get("code"),
        phoneNCC=nccRequest.get("phoneNCC"),
        emailNCC=nccRequest.get("emailNCC")
    )
    return JsonResponse({"message": "Thêm nhà cung cấp thành công", "model": model_to_dict(ncc)}, status=200)
@csrf_exempt
@require_http_methods(["POST"])
def addCustomer(request):
    data = json.loads(request.body)
    customerRequest=data.get("customer")
    if Customer.objects.filter(name=customerRequest.get("name")).exists():
        return JsonResponse({"message":"Customer đã tồn tại!","success":False ,"model": model_to_dict(Customer.objects.get(name=customerRequest.get("name")))}, status=400)
    customer=Customer.objects.create(
        name=customerRequest.get("name"),
        code=customerRequest.get("code"),
        phone=customerRequest.get("phone"),
        email=customerRequest.get("email"),
        address=customerRequest.get("address"),
    )
    return JsonResponse({"message": "Thêm nhà cung cấp thành công", "success": True,"customer": model_to_dict(customer) }, status=200)
@csrf_exempt
@require_http_methods(["GET"])
def getCustomer(request,customer_id=None):
    if customer_id is None:
        customers = list(Customer.objects.values())
        return JsonResponse({"success": True, "customers": customers}, status=200)
    else :
        try:
            customer = Customer.objects.get(id=customer_id)
            return JsonResponse({"success": True, "customer": model_to_dict(customer)}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
@csrf_exempt
@require_http_methods(["GET"])
def getNCC(request,customer_id=None):
    if customer_id is None:
        nhaCungCap = list(NhaCungCap.objects.values())
        return JsonResponse({"success":True,"NhaCungCap": nhaCungCap}, status=200)
    else :
        try:
            customer = NhaCungCap.objects.get(id=customer_id)
            return JsonResponse({"success": True, "customer": model_to_dict(customer)}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
@csrf_exempt
@require_http_methods(["POST"])
@transaction.atomic
def addPhieuNhap(request):
    data = json.loads(request.body)
    customerRequest = data.get("codeCustomer")

    try:
        customer = Customer.objects.get(code=customerRequest)

        phieuXuatRequest = data.get("phieuXuat")
        listChiTietPhieuXuat = data.get("chiTietPhieuXuat")

        # **Bước 1: Kiểm tra toàn bộ danh sách trước khi tạo phiếu xuất**
        for item in listChiTietPhieuXuat:
            if not Product.objects.filter(code=item.get("codeProduct")).exists():
                return JsonResponse({"message": f"Không có sản phẩm {item.get('codeProduct')}", "success": False}, status=400)

            product = Product.objects.get(code=item.get("codeProduct"))
            if product.quantity < item.get("quantity"):
                return JsonResponse({
                    "message": "Số lượng sản phẩm không đủ",
                    "success": False,
                    "model": model_to_dict(product)
                }, status=400)

        # **Bước 2: Tạo phiếu xuất vì không có lỗi nào**
        with transaction.atomic():
            phieuXuat = PhieuXuat.objects.create(
                date=phieuXuatRequest.get("date"),
                totalPrice=phieuXuatRequest.get("totalPrice"),
                notes=phieuXuatRequest.get("notes"),
                customer=customer
            )

            # **Bước 3: Lưu chi tiết phiếu xuất**
            for item in listChiTietPhieuXuat:
                product = Product.objects.get(code=item.get("codeProduct"))

                ChiTietPhieuXuat.objects.create(
                    quantity=item.get("quantity"),
                    sellingPrice=item.get("sellingPrice"),
                    product=product,
                    phieuXuat=phieuXuat
                )
                # **Cập nhật số lượng sản phẩm**
                product.quantity -= item.get("quantity")
                product.save()

        return JsonResponse({"message": "Thêm phiếu xuất thành công", "success": True})

    except Customer.DoesNotExist:
        return JsonResponse({"message": "Khách hàng không tồn tại", "success": False}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)
@csrf_exempt
@require_http_methods(["POST"])
def updateProduct(request):
    data = json.loads(request.body)
    try:
        with transaction.atomic():
            product = Product.objects.get(code=data.get("code"))
            product.sellingPrice = data.get("sellingPrice")
            product.notes = data.get("notes")
            product.name = data.get("nameProduct")
            product.category = data.get("category")
            product.save()
            return JsonResponse( {"message":"thành công","success":True},status=200)
    except Product.DoesNotExist:
        return JsonResponse({"message":"không thành công", "success": False}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def home_manager(request):
    products = list(Product.objects.filter(quantity__lt=20).order_by('quantity').values())
    return JsonResponse({"products": products, "success": True})

@csrf_exempt
@require_http_methods(["GET"])
def export_products_excel(request):
    # Tạo file Excel mới
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Products"

    # Tiêu đề cột
    headers = ["ID", "Code", "Name", "Category", "Import Price", "Selling Price", "Quantity", "Notes"]
    ws.append(headers)

    # Lấy dữ liệu từ database và thêm vào Excel
    for product in Product.objects.all():
        ws.append([
            product.id, product.code, product.nameProduct, product.category,
            product.importPrice, product.sellingPrice, product.quantity, product.notes
        ])

    # Trả về file Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="products.xlsx"'
    wb.save(response)

    return response