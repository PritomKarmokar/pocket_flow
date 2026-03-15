# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Module imports
from authentication.models import User, Account

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # Fields visible in user list page
    list_display = (
        "id",
        "email",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_email_verified",
        "created_at",
    )

    search_fields = (
        "email",
        "username",
        "display_name",
        "mobile_number",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "last_active",
        "last_login",
        "date_joined",
    )

    fieldsets = (
        ("Authentication", {
            "fields": (
                "id",
                "email",
                "username",
                "password",
            )
        }),

        ("Personal Info", {
            "fields": (
                "display_name",
                "first_name",
                "last_name",
                "mobile_number",
                "user_timezone",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_email_verified",
                "groups",
                "user_permissions",
            )
        }),

        ("Security", {
            "fields": (
                "is_password_expired",
                "is_password_autoset",
                "is_password_reset_required",
            )
        }),

        ("Activity", {
            "fields": (
                "last_active",
                "last_login_time",
                "last_logout_time",
            )
        }),

        ("Important Dates", {
            "fields": (
                "created_at",
                "updated_at",
                "date_joined",
            )
        }),
    )

    # Fields shown when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "password1",
                "password2",
                "is_staff",
                "is_superuser",
                "is_active",
            ),
        }),
    )


admin.site.register(Account)