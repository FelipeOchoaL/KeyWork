from django.contrib import admin
from .models import EmailHistory

@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ('recipient_email', 'user', 'sent_at', 'status')
    list_filter = ('status', 'sent_at')
    search_fields = ('recipient_email', 'user__username')
    date_hierarchy = 'sent_at'