from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    BasePermission,
    SAFE_METHODS
)

class GetAndPostCustomPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method == "GET":
            return True
        else:
            return bool(request.user and request.user.is_admin)