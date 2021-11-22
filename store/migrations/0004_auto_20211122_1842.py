# Generated by Django 2.2.12 on 2021-11-22 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20211122_1835'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(price__gt=0), name='price_gt_0'),
        ),
    ]