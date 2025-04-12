# Generated by Django 4.2.20 on 2025-04-12 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_alter_log_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='phieunhap',
            name='status',
            field=models.CharField(choices=[('pending', 'Chờ xử lý'), ('completed', 'Hoàn thành'), ('canceled', 'Đã hủy')], default='pending', max_length=20),
        ),
    ]
