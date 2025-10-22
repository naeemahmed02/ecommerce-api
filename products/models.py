from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=1100, unique=True)
    product_description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.ImageField(upload_to='products')
    