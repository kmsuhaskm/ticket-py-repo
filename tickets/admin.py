from django.contrib import admin
from .models import Ticket, TicketReply

class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 0

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at']
    list_filter = ['status']
    inlines = [TicketReplyInline]  # ✅ show replies in ticket admin view

@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'message', 'created_at']
    list_filter = ['ticket', 'user']
