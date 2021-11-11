from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=100)
    stock_count = models.IntegerField(help_text="How many items are currently in stock.")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(default="", blank=True)
    sku = models.CharField(verbose_name="Stock Keeping Unit", max_length=20, unique=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('store:product-detail', kwargs={'pk': self.id})


class ProductImage(models.Model):
    image = models.ImageField()
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

