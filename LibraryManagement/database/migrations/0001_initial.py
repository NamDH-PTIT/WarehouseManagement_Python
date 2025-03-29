# Generated by Django 4.2.20 on 2025-03-26 16:29

import database.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=database.models.generate_unique_code, max_length=20, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='NhaCungCap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('nameNCC', models.CharField(max_length=20)),
                ('addressNCC', models.CharField(max_length=20)),
                ('phoneNCC', models.CharField(max_length=20)),
                ('emailNCC', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=database.models.generate_unique_code, max_length=20, unique=True)),
                ('nameProduct', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=20)),
                ('importPrice', models.FloatField()),
                ('sellingPrice', models.FloatField(blank=True, null=True)),
                ('quantity', models.IntegerField()),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.role')),
            ],
        ),
        migrations.CreateModel(
            name='PhieuXuat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=database.models.generate_unique_code, max_length=20, unique=True)),
                ('date', models.DateTimeField()),
                ('totalPrice', models.FloatField()),
                ('notes', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Chờ xử lý'), ('completed', 'Hoàn thành'), ('canceled', 'Đã hủy')], default='pending', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.customer', to_field='code')),
            ],
        ),
        migrations.CreateModel(
            name='PhieuNhap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=database.models.generate_unique_code, max_length=20, unique=True)),
                ('date', models.DateTimeField()),
                ('totalPrice', models.FloatField()),
                ('notes', models.TextField()),
                ('codeNCC', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.nhacungcap', to_field='code')),
            ],
        ),
        migrations.CreateModel(
            name='ChiTietPhieuXuat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('sellingPrice', models.FloatField()),
                ('phieuXuat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.phieuxuat', to_field='code')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.product', to_field='code')),
            ],
        ),
        migrations.CreateModel(
            name='ChiTietPhieuNhap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('importPrice', models.FloatField()),
                ('codePhieuNhap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.phieunhap', to_field='code')),
                ('codeProduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.product', to_field='code')),
            ],
        ),
    ]
