from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class CustomAccountManager(BaseUserManager):

    # method to create common user
    def create_user(
        self,
        first_name,
        last_name,
        email,
        username,
        phone_number=None,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("user must have a valid email address")
        if not username:
            raise ValueError("User must have a valid username")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            **extra_fields,
        )

        # set password
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)

    # System Flags
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
