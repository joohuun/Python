from django.db import models
from django.db.models import Q, QuerySet
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.models import _user_has_perm
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    Permission,  
    PermissionsMixin,
    )
from permissions import AccountPermissions, BasePermissionEnum, get_permissions

class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def customers(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & Q(orders__isnull=False))
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


# class User(PermissionsMixin, ModelWithMetadata, AbstractBaseUser):
class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    hashed_email = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    # addresses = models.ManyToManyField(
    #     Address, blank=True, related_name="user_addresses"
    # )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    withdraw_block = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    # default_shipping_address = models.ForeignKey(
    #     Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    # )
    # default_billing_address = models.ForeignKey(
    #     Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    # )
    # avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    jwt_token_key = models.CharField(max_length=12, default=get_random_string)
    login_fail_count = models.IntegerField(default=0)
    # dormant_status = models.CharField(max_length=11, blank=True, choices=DormantStatus.CHOICES)
    sha_password = models.CharField(max_length=256, blank=True, null=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ("email",)
        permissions = (
            (AccountPermissions.MANAGE_USERS.codename, "Manage customers."),
            (AccountPermissions.MANAGE_STAFF.codename, "Manage staff."),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effective_permissions = None

    @property
    def effective_permissions(self) -> "QuerySet[Permission]":
        if self._effective_permissions is None:
            self._effective_permissions = get_permissions()
            if not self.is_superuser:
                self._effective_permissions = self._effective_permissions.filter(
                    Q(user=self) | Q(group__user=self)
                )
        return self._effective_permissions

    @effective_permissions.setter
    def effective_permissions(self, value: "QuerySet[Permission]"):
        self._effective_permissions = value
        # Drop cache for authentication backend
        self._effective_permissions_cache = None

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        if self.default_billing_address:
            first_name = self.default_billing_address.first_name
            last_name = self.default_billing_address.last_name
            if first_name or last_name:
                return f"{first_name} {last_name}".strip()
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm: Union[BasePermissionEnum, str], obj=None):  # type: ignore
        # This method is overridden to accept perm as BasePermissionEnum
        perm = perm.value if hasattr(perm, "value") else perm  # type: ignore

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser and not self._effective_permissions:
            return True
        return _user_has_perm(self, perm, obj)