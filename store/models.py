from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ProductStockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stock_count__gt=0)


class ProductGotName(models.QuerySet):
    def get_name(self):
        return self.filter(name__contains='tv')


class Product(models.Model):
    name = models.CharField(max_length=100)
    stock_count = models.IntegerField(help_text="How many items are currently in stock.")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(default="", blank=True)
    sku = models.CharField(verbose_name="Stock Keeping Unit", max_length=20, unique=True)
    slug = models.SlugField()

    # Applying custom manager
    objects = models.Manager()  # To keep default 'objects' manager (without custom manager we don't need it)
    in_stock = ProductStockManager()    # To make custom manager
    get_name_query = ProductGotName.as_manager()  # Another approach to filter products

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('store:product-detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['name', '-price']   # '-' - DESC sort
        db_table = 'Vacuums'    # Renames table in db (default class name)
        constraints = [models.CheckConstraint(check=models.Q(price__gt=0), name='Price_gt_0'),
                       models.CheckConstraint(check=(~models.Q(description__icontains='sony')), name="Sony_check")]
    # A list of constraints that you want to define on the model


class DigitalProduct(Product):
    file = models.FileField()

#
# class PhysicalProduct(Product):
#     stock_count = models.IntegerField(help_text="How many items are currently in stock.")


class ProductImage(models.Model):
    image = models.CharField(max_length=100)
    # image = models.ImageField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.image}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField('Product', related_name='categories')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

