from django.db import models
from core.models import Base
from category.models import Category


class Product(Base):
    name = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=1100, unique=True)
    product_description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.ImageField(upload_to='products')
    stock = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tax = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    

