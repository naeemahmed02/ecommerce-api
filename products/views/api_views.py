from .. models import Product
from .. serializers import ProductSerializer
from rest_framework import generics, permissions

class ProductListAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)



class RetrieveUpdateDestroyAPIViewAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
