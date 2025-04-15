import uuid

from django.db import models


def generate_unique_code():
    return str(uuid.uuid4())[:50]  # Cắt 50 ký tự đầu tiên từ UUID


# Create your models here.
class Kho(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    notes = models.TextField()


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True, default=generate_unique_code)
    nameProduct = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    importPrice = models.FloatField()
    sellingPrice = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    codeKho = models.ForeignKey(Kho, to_field='code', on_delete=models.CASCADE, related_name='products')
    notes = models.TextField()


class NhaCungCap(models.Model):
    code = models.CharField(max_length=50, unique=True,default=generate_unique_code)
    nameNCC = models.CharField(max_length=50)
    addressNCC = models.CharField(max_length=50)
    phoneNCC = models.CharField(max_length=50)
    emailNCC = models.CharField(max_length=50)
    notes = models.TextField(blank=True)


class PhieuNhap(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('completed', 'Hoàn thành'),
        ('canceled', 'Đã hủy'),
    ]
    code = models.CharField(max_length=50, unique=True, default=generate_unique_code)
    date = models.DateTimeField()
    totalPrice = models.FloatField()
    notes = models.TextField()
    codeKho = models.ForeignKey(Kho, to_field='code', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    codeNCC = models.ForeignKey(NhaCungCap, to_field='code', on_delete=models.CASCADE)


class ChiTietPhieuNhap(models.Model):
    codeProduct = models.ForeignKey(Product, to_field="code", on_delete=models.CASCADE)
    codePhieuNhap = models.ForeignKey(PhieuNhap, to_field="code", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    importPrice = models.FloatField()


class Customer(models.Model):
    code = models.CharField(max_length=50, unique=True, default=generate_unique_code)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    status =models.CharField(max_length=50,blank=True)

class PhieuXuat(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('completed', 'Hoàn thành'),
        ('canceled', 'Đã hủy'),
    ]
    code = models.CharField(max_length=50, unique=True, default=generate_unique_code)
    date = models.DateTimeField()
    totalPrice = models.FloatField()
    notes = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    customer = models.ForeignKey(Customer, to_field="code", on_delete=models.CASCADE)


class ChiTietPhieuXuat(models.Model):
    quantity = models.IntegerField()
    sellingPrice = models.FloatField()
    phieuXuat = models.ForeignKey(PhieuXuat, to_field="code", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, to_field="code", on_delete=models.CASCADE)


class Role(models.Model):
    name = models.CharField(max_length=50)


class User(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Log(models.Model):
    notes = models.TextField()
    date = models.DateTimeField()
    user=models.TextField(blank=True)
