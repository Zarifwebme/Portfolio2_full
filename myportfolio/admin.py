from django.contrib import admin
from .models import Project, ContactMessage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "button_type", "is_active", "order", "created_at")
    list_filter = ("category", "is_active", "button_type")
    search_fields = ("title", "stack", "description")
    list_editable = ("is_active", "order")
    fields = ("category", "title", "description", "stack", "image", "button_type", "button_url", "is_active", "order")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "phone", "message")
    list_editable = ("is_read",)