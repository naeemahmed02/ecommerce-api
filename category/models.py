from django.db import models
from core.models import Base

class Category(Base):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=120)