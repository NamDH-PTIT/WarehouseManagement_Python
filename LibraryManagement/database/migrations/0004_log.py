# Generated by Django 4.2.20 on 2025-03-25 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_phieuxuat_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
