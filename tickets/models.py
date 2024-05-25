from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
        ('Open', 'Open'),
    )
    title = models.CharField(max_length=300, blank=False, null=False, verbose_name="Title")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="tickets")
    description = models.TextField(blank=False, null=False, verbose_name="Description")
    assigned_to = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='assignments', blank=True,
                                    null=True, verbose_name="Assigned to")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    accepted_at = models.DateTimeField(blank=True, null=True, verbose_name="Accepted at")
    closed_at = models.DateTimeField(blank=True, null=True, verbose_name="Closed at")
    closed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,blank=True, related_name="closed_tickets", verbose_name="closed by")
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default="Open", verbose_name="Status")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ticket_detail',args=[self.id])

class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="messages")
    message = models.TextField(blank=False, null=False, verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

