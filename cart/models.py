from django.db import models
from accounts.models import Account
from products.models import Product, ProductVariations


class Cart(models.Model):
    cart_id = models.CharField(max_length=100)
    cart_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(ProductVariations)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    def __str__(self):
        return self.product.name
