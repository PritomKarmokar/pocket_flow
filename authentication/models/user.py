# Python imports
import pytz
import ulid
import random
import string

# Django imports
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

# Module imports
from applibs.mixins import TimeAuditModel

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=26, unique=True, editable=False, primary_key=True)
    username = models.CharField(max_length=128)

    # user fields
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, null=True, blank=True, unique=True)

    # identity
    display_name = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    # tracking metrics
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date Joined")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    last_location = models.CharField(max_length=255, blank=True)
    created_location = models.CharField(max_length=255, blank=True)


    # ths is' es
    is_superuser = models.BooleanField(default=False)
    is_password_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_password_autoset = models.BooleanField(default=False)
    is_password_reset_required = models.BooleanField(default=False)

    last_active = models.DateTimeField(default=timezone.now, null=True)
    last_login_time = models.DateTimeField(null=True)
    last_logout_time = models.DateTimeField(null=True)

    # timezone
    USER_TIMEZONE_CHOICES = tuple(zip(pytz.common_timezones, pytz.common_timezones))
    user_timezone = models.CharField(max_length=255, choices=USER_TIMEZONE_CHOICES, default="UTC")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.username} <{self.email}>"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(ulid.ULID())

        self.email = self.email.lower().strip()
        self.mobile_number = self.mobile_number

        if not self.display_name:
            self.display_name = (
                self.email.split("@")[0]
                if len(self.email.split("@"))
                else "".join(random.choice(string.ascii_letters) for _ in range(6))
            )
        if self.is_superuser:
            self.is_staff = True

        super(User, self).save(*args, **kwargs)

    @classmethod
    def get_display_name(cls, email: str) -> str:
        if not email:
            return "".join(random.choice(string.ascii_letters) for _ in range(6))
        return (
            email.split("@")[0]
            if len(email.split("@")) == 2
            else "".join(random.choice(string.ascii_letters) for _ in range(6))
        )

class Account(TimeAuditModel):
    PROVIDER_CHOICES = (
        ("google", "Google"),
        ("facebook", "Facebook"),
        ("github", "Github"),
    )
    id = models.CharField(max_length=26, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="accounts")
    provider_account_id = models.CharField(max_length=255)
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)
    access_token = models.TextField()
    access_token_expired_at = models.DateTimeField(null=True)
    refresh_token = models.TextField(null=True, blank=True)
    refresh_token_expired_at = models.DateTimeField(null=True)
    last_connected_at = models.DateTimeField(default=timezone.now)
    id_token = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        unique_together = ["provider", "provider_account_id"]
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        db_table = "accounts"
        ordering = ("-created_at",)