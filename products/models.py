from django.db import models
from core.models import Base
from category.models import Category
from decimal import Decimal
from django.urls import reverse


class Product(Base):
    """
    Represents a product available for sale in the store.

    Attributes:
        name (str): The name of the product.
        slug (str): A URL-friendly version of the product name, unique per product.
        product_description (str): A detailed description of the product (optional).
        price (Decimal): The base price of the product before tax.
        image (ImageField): The main image associated with the product.
        stock (int): The number of items available in inventory.
        in_stock (bool): Indicates if the product is currently in stock.
        category (Category): The category this product belongs to.
        tax (Decimal): The tax rate applied to this product, represented as a decimal (e.g., 0.10 for 10%).
    """
    name = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=1100, unique=True)
    product_description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    stock = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tax = models.DecimalField(max_digits=3, decimal_places=2)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("name",)

    def calculate_total_with_tax(self):
        """
        Calculates the total product price including tax.

        Returns:
            Decimal: The total price after applying the tax rate.
                     For example, if price=100 and tax=0.10, returns 110.00.
        """
        return self.price * (Decimal("1.00") + self.tax)

    @property
    def total_with_tax(self):
        """
        Returns the total price including tax as a property.

        This allows you to access the value as an attribute (e.g., product.total_with_tax)
        instead of calling a method (e.g., product.calculate_total_with_tax()).

        Returns:
            Decimal: The total price after applying the tax rate.
        """
        return self.calculate_total_with_tax()

    @property
    def get_absolute_url(self):
        return reverse("api_single_product", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


variation_category_choice = (("color", "COLOR"), ("size", "SIZE"))


class ProductVariations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Variation"
        verbose_name_plural = "Variations"

    def __str__(self):
        return self.variation_value