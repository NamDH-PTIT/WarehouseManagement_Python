import uuid

from django.db import models
def generate_unique_code():
    return str(uuid.uuid4())[:20]  # Cắt 20 ký tự đầu tiên từ UUID
# Create your models here.
class Product(models.Model):
    code =models.CharField(max_length=20, unique=True,default=generate_unique_code)
    nameProduct= models.CharField(max_length=20)
    category= models.CharField(max_length=20)
    importPrice= models.FloatField()
    sellingPrice = models.FloatField(null=True, blank=True)
    quantity= models.IntegerField()
    notes= models.TextField()
class NhaCungCap(models.Model):
    code =models.CharField(max_length=20, unique=True)
    nameNCC= models.CharField(max_length=20)
    addressNCC= models.CharField(max_length=20)
    phoneNCC= models.CharField(max_length=20)
    emailNCC= models.CharField(max_length=20)

class PhieuNhap(models.Model):
    code =models.CharField(max_length=20, unique=True,default=generate_unique_code)
    date= models.DateTimeField()
    totalPrice= models.FloatField()
    notes= models.TextField()
    codeNCC=models.ForeignKey(NhaCungCap,to_field='code',on_delete=models.CASCADE)

class ChiTietPhieuNhap(models.Model):
    codeProduct=models.ForeignKey(Product,to_field="code",on_delete=models.CASCADE)
    codePhieuNhap=models.ForeignKey(PhieuNhap,to_field="code",on_delete=models.CASCADE)
    quantity= models.IntegerField()
    importPrice= models.FloatField()


class Customer(models.Model):
    code =models.CharField(max_length=20, unique=True,default=generate_unique_code)
    name =models.CharField(max_length=20)
    address =models.CharField(max_length=20)
    phone =models.CharField(max_length=20)
    email =models.CharField(max_length=20)

class PhieuXuat(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('completed', 'Hoàn thành'),
        ('canceled', 'Đã hủy'),
    ]
    code =models.CharField(max_length=20, unique=True,default=generate_unique_code)
    date= models.DateTimeField()
    totalPrice= models.FloatField()
    notes= models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    customer= models.ForeignKey(Customer,to_field="code",on_delete=models.CASCADE)

class ChiTietPhieuXuat(models.Model):
    quantity= models.IntegerField()
    sellingPrice= models.FloatField()
    phieuXuat=models.ForeignKey(PhieuXuat,to_field="code",on_delete=models.CASCADE)
    product= models.ForeignKey(Product,to_field="code",on_delete=models.CASCADE)
class Role(models.Model):
    name =models.CharField(max_length=20)

class User(models.Model):
    code =models.CharField(max_length=20, unique=True)
    name =models.CharField(max_length=20)
    address =models.CharField(max_length=20)
    phone =models.CharField(max_length=20)
    email =models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    role= models.ForeignKey(Role,on_delete=models.CASCADE)
class Log(models.Model):
    notes= models.TextField()
    date= models.DateTimeField()




