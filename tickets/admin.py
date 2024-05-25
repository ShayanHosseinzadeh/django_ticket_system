from django.contrib import admin

from tickets.models import Ticket, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'assigned_to', 'created_at', 'status']
    search_fields = ['id', 'title']
    list_display_links = ['title']
    list_editable = ['status']
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'message']
