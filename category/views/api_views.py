from dns.e164 import query
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from ..models import Category
from ..serializers import CategorySerializer
from products.custom_permissions import GetAndPostCustomPermission


class CategoryCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [GetAndPostCustomPermission]

    def get_queryset(self):
        queryset = Category.objects.all()

    def perform_create(self, serializer):
        # set the current user
        current_user = self.request.user

        # check if the current user is an admin or staff user
        if not current_user.is_staff and current_user.is_admin:
            raise PermissionDenied("You are not allowed to access this resource")
