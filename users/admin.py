from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from projects.models import Project

User = get_user_model()


class ProjectInLine(admin.StackedInline):
    model = Project
    extra = 0


@admin.register(User)
class MyUserAdmin(BaseUserAdmin):
    model = User

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (("Дополнительная информация"),
         {"fields": (
             "name", "surname", "phone", "avatar", "about", "favorites")}),
        (
            ("Права"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Важные даты"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email", "password"),
            },
        ),
    )
    list_display = (
        'email', 'name', 'surname', 'phone', 'github_url', 'is_staff',
        'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ("email", "name", "surname", "phone")
    empty_value_display = 'Не задано'
    list_editable = (
        'name', 'surname', 'github_url', 'is_staff', 'is_active', 'phone')
    filter_horizontal = ('favorites',)
    inlines = (
        ProjectInLine,
    )
