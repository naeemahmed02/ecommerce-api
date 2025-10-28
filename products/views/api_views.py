from ..models import Product
from ..serializers import ProductSerializer
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from ..custom_permissions import GetAndPostCustomPermission


class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [GetAndPostCustomPermission]

    def get_queryset(self):
        # filter active products
        return Product.objects.filter(is_active=True)

    def perform_create(self, serializer):
        # current user
        current_user = self.request.user
        # check if the user is the owner of the store (staff or admin)
        if not current_user.is_admin:
            raise PermissionDenied("You are not allowed to access this resource")
        serializer.save()


class RetrieveUpdateDestroyAPIViewAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
