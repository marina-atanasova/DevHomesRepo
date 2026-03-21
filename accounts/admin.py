from django.contrib import admin

from .models import UserInquiry


@admin.register(UserInquiry)
class UserInquiryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'listing', 'posted_by', 'status', 'created_at')
    list_filter = ('status', 'request_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')