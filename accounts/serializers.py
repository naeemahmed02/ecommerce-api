from rest_framework import serializers
from accounts.models import Account

class AccountRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user account.
    """
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'username', 'password']

    def create(self, validated_data):
        """
        Create a new inactive user account from validated data.
        """
        user = Account.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user


class AccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'password')