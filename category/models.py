from django.db import models
from core.models import Base


class Category(Base):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=120)
    category_description = models.TextField()
    category_image = models.ImageField(upload_to="categories", null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
