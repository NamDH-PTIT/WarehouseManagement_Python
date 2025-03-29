import json
from datetime import datetime, timedelta
import random

import openpyxl
from django.core.mail import send_mail
from django.db import transaction
from django.db.models.aggregates import Sum
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from unicodedata import category

from LibraryManagement import settings
from database.models import *
from warehouse_management.response.ApiResponse import ApiResponse



# Create your views here.
@require_http_methods(["GET"])
@require_http_methods(["GET"])
@csrf_exempt
def getAllProducts(request):
    products = list(Product.objects.raw("select * from database_product order by quantity asc"))
    page=int(request.GET.get('page', 1))-1
    low_stock_products = Product.objects.filter(quantity__lt=30)
    pagequantity=int(len(products)/10)
    danhmuc =list(Product.objects.raw("SELECT category,id FROM `database_product` GROUP BY category"))
    if(len(products)%10!=0):
        pagequantity+=1
    return render(request, 'LibraryManagement/quanlyproduct.html', {"products":products[page*10:page*10+10],"sanphamsaphet":low_stock_products,"page":range(1,pagequantity+1),"nowpage":page+1,"danhmuc":danhmuc})
@require_http_methods(["GET"])
@csrf_exempt
def editProduct(request,product_id):
    product = get_object_or_404(Product.objects.values(), code=product_id)  # Tìm sản phẩm theo code, nếu không có thì trả về 404
    return render(request,"LibraryManagement/editProduct.html",{"product":product})

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
def getCustomer(request,customer_code=None):
    if customer_code is None:
        customers = list(Customer.objects.values())
        return JsonResponse({"success": True, "customers": customers}, status=200)
    else :
        try:
            customer = Customer.objects.get(code=customer_code)
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
def addPhieuXuat(request):
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
                Log.objects.create(
                    date=datetime.now() ,
                    notes="xử lý phiếu xuất"+phieuXuat.code
                )

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
    low_stock_products = Product.objects.filter(quantity__lt=30)
    phieuxuat=PhieuXuat.objects.filter(status="completed")
    loinhuan=0
    for item in phieuxuat:
        chitietpx=ChiTietPhieuXuat.objects.filter(phieuXuat=item)
        for x in chitietpx:
            tong=(x.sellingPrice-x.product.importPrice)*x.quantity
            loinhuan=tong
    doanhthu = PhieuXuat.objects.filter(status="completed").aggregate(Sum('totalPrice'))['totalPrice__sum']
    products = Product.objects.all()
    pxt=[]
    for i in range(1,13):
        pxt.append(PhieuXuat.objects.filter(date__month=i).count())
    phieuxuat=PhieuXuat.objects.filter(status="pending")
    log = Log.objects.order_by('-date')[:5]
    return render(request,'LibraryManagement/home_manager.html',{"pxt":pxt,"phieuxuat":phieuxuat,"soluongpx":phieuxuat.count(),"products":products.count(),"log":log,"doanhthu":doanhthu,"loinhuan":loinhuan,"sanphamsaphet":low_stock_products})
@csrf_exempt
@require_http_methods(["POST"])
def export_products_excel(request):
    data=json.loads(request.body)
    category=data.get("category")
    status = data.get("status")
    sort = data.get("sort")
    search = data.get("search")
    products = Product.objects.all()

    if category:
        products = products.filter(category=category)
    if status:
        if status == "2":
            products = products.filter(quantity__gte=1)
        if status == "3":
            products = products.filter(quantity__lte=20)
        if status == "4":
            products = products.filter(quantity__lte=0)
    if search:
        products = products.filter(nameProduct__icontains=search)

    # Sắp xếp theo sort
    if sort == 'name-asc':
        products = products.order_by('nameProduct')
    if sort == 'name-desc':
        products = products.order_by('-nameProduct')
    if sort == "price-asc":
        products = products.order_by("sellingPrice")  # Sắp xếp tăng dần
    if sort == "price-desc":
        products = products.order_by("-sellingPrice")  # Sắp xếp giảm dần
    # Tạo file Excel mới
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Products"

    # Tiêu đề cột
    headers = ["ID", "Code", "Name", "Category", "Import Price", "Selling Price", "Quantity", "Notes"]
    ws.append(headers)

    # Lấy dữ liệu từ database và thêm vào Excel
    for product in products:
        ws.append([
            product.id, product.code, product.nameProduct, product.category,
            product.importPrice, product.sellingPrice, product.quantity, product.notes
        ])

    # Trả về file Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="products.xlsx"'
    wb.save(response)

    return response
@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(email=email).first()
        if user is None or user.password!=password:
            return render(request, "LibraryManagement/login.html",{"message":"tài khoản hoặc mật khẩu không chính xác"})
        else:
            if user.role.name=="Admin":
                request.session["user_id"] =user.code
                return redirect('home_manager/')
            else:
                request.session["user_id"] = user.code
                return render(request, "LibraryManagement/index.html.html")
    elif request.method == "GET" :
        return render(request, "LibraryManagement/login.html",)

def send_email(sub,mess,email):
    subject = sub
    message = mess
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
@csrf_exempt
@require_http_methods(["POST"])
def forgot(request):
    data=request.POST.get("email")
    if(User.objects.filter(email=data).first() is None):
        return JsonResponse({"success": False,"message":"email không tồn tại"},status=200)
    otp = random.randint(100000, 999999)
    user=User.objects.filter(email=data).first()
    expiry_time = datetime.now() + timedelta(minutes=5)
    request.session["user_code"] = user.code
    request.session["otp"] = otp
    request.session["otp_expiry"] = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
    send_email("mã OTP","OTP : "+str(otp),data)
    return JsonResponse({"success": True},status=200)
@csrf_exempt
@require_http_methods(["POST"])
def verify_otp(request):
    user_otp = request.POST.get("otp")  # OTP nhập từ người dùng
    session_otp = request.session.get("otp")  # OTP trong session
    otp_expiry = request.session.get("otp_expiry")  # Thời gian hết hạn
    if not session_otp or not otp_expiry:
        return JsonResponse({"message": "OTP không tồn tại hoặc đã hết hạn!", "success": False}, status=400)
    otp_expiry_time = datetime.strptime(otp_expiry, "%Y-%m-%d %H:%M:%S")
    if datetime.now() > otp_expiry_time:
        return JsonResponse({"message": "OTP đã hết hạn!", "success": False}, status=400)

    if str(user_otp) != str(session_otp):
        return JsonResponse({"message": "OTP không hợp lệ!", "success": False}, status=400)

    # Xóa OTP khỏi session sau khi xác minh thành công
    return JsonResponse({"message": "Xác minh thành công!", "success": True})
@csrf_exempt
@require_http_methods(["POST"])
def updatepassword(request):
    password=request.POST.get("password")
    user_code=request.session.get("user_code")
    User.objects.filter(code=user_code).update(password=password)
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request,product_code=None):
    product = get_object_or_404(Product, code=product_code)
    product.delete()
    return JsonResponse({"success": True})
@csrf_exempt
@require_http_methods(["GET"])
def filter_products(request):
    category = request.GET.get('category')
    sort = request.GET.get('sort')
    status = request.GET.get('status')
    search = request.GET.get('search')


    # Kiểm tra nếu request không có dữ liệu

    # Lọc sản phẩm
    products = Product.objects.all()

    if category:
        products = products.filter(category=category)
    if status:
        if status == "2":
            products = products.filter(quantity__gte=1)
        if status == "3":
            products = products.filter(quantity__lte=20)
        if status == "4":
            products = products.filter(quantity__lte=0)
    if search:
        products = products.filter(nameProduct__icontains=search)

    # Sắp xếp theo sort
    if sort == 'name-asc':
        products = products.order_by('nameProduct')
    if sort == 'name-desc':
        products = products.order_by('-nameProduct')
    if sort == "price-asc":
        products = products.order_by("sellingPrice")  # Sắp xếp tăng dần
    if sort == "price-desc":
        products = products.order_by("-sellingPrice")  # Sắp xếp giảm dần

    # Trả về JSON để kiểm tra
    data = list(products.values())
    danhmuc = list(Product.objects.raw("SELECT category,id FROM `database_product` GROUP BY category"))
    return render(request,"LibraryManagement/quanlyproduct.html",{"products":products,"danhmuc":danhmuc})

