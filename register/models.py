from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group,
    Permission,
)
from django.utils.translation import gettext as _
from django.db import models
from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=10,
    )
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    account_no = models.PositiveIntegerField(unique=True, null=True)
    default_currency = models.CharField(
        max_length=3,
        choices=[("GBP", "GBP"), ("EUR", "EUR"), ("NGN", "NGN"), ("USD", "USD")],
        default="USD",
    )
    balance = models.DecimalField(default=1000.00, max_digits=12, decimal_places=2)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
        related_name="customuser_set",  # add related_name argument
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="customuser_set",  # add related_name argument
        related_query_name="user",
    )
