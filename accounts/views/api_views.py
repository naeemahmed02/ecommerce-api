from rest_framework import generics, status
from ..serializers import AccountRegisterationSerializer, AccountLoginSerializer
from rest_framework.permissions import AllowAny
from accounts.models import Account
from django.contrib.auth import authenticate
from rest_framework.response import Response

class AccountRegisterationAPIView(generics.CreateAPIView):
    serializer_class = AccountRegisterationSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Account.objects.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(is_active=True)


class AccountLoginAPIView(generics.GenericAPIView):
    serializer_class = AccountLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate user
        user = authenticate(email=email, password=password)

        if not user:
            return Response({'message': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Successfully logged in.'}, status=status.HTTP_200_OK)
