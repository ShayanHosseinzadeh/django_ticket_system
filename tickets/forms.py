from django import forms

from tickets.models import Ticket, Message


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message',)
