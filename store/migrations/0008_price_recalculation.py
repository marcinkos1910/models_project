# Generated by Django 2.2.12 on 2021-11-22 20:22
from decimal import Decimal

from django.db import migrations


def calculate_eur(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    for p in Product.objects.all():
        p.price = p.price / Decimal('4.7')
        p.save()


def undo_calculation(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    for p in Product.objects.all():
        p.price = p.price / Decimal('4.7')
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20211122_1903'),
    ]

    operations = [
        migrations.RunPython(calculate_eur, reverse_code=undo_calculation)
    ]
