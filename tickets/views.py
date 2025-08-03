from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic

from .forms import TicketForm
from .models import Ticket, Message


class IndexView(generic.TemplateView):
    """
    A simple view to render the homepage.
    """
    template_name = 'tickets/index.html'


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    """
    A view to handle the creation of a new ticket.
    LoginRequiredMixin ensures that only authenticated users can create tickets.
    """
    template_name = 'tickets/createticket.html'
    form_class = TicketForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        Automatically sets the user of the new ticket to the currently logged-in user.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketListView(LoginRequiredMixin, generic.ListView):
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        is_admin = user.groups.filter(name='Admin').exists() or user.is_superuser
        is_support = user.groups.filter(name='support').exists()

        if is_admin:
            context['open_tickets'] = Ticket.objects.filter(status='Open')
            context['pending_tickets'] = Ticket.objects.filter(status='Pending')
            context['closed_tickets'] = Ticket.objects.filter(status='Closed')
        elif is_support:
            context['open_tickets'] = Ticket.objects.filter(status='Open')
            context['pending_tickets'] = Ticket.objects.filter(
                Q(status='Pending') |
                (Q(assigned_to=user) & ~Q(status='Closed'))
            )
            context['closed_tickets'] = Ticket.objects.filter(
                Q(status='Closed') &
                (Q(user=user) | Q(assigned_to=user))
            )
        else:
            context['open_tickets'] = Ticket.objects.filter(status='Open', user=user)
            context['pending_tickets'] = Ticket.objects.filter(status='Pending', user=user)
            context['closed_tickets'] = Ticket.objects.filter(status='Closed', user=user)

        context['role'] = [role.name for role in user.groups.all()]
        return context


class TicketDetailView(UserPassesTestMixin, LoginRequiredMixin, generic.DetailView):
    """
    A view to display the details of a single ticket and handle new messages.
    """
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        """
        Adds all messages related to the current ticket to the context.
        """
        context = super().get_context_data(**kwargs)
        context['ticket_messages'] = Message.objects.filter(ticket=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the creation of a new message for the ticket.
        """
        ticket = self.get_object()
        ticket_message = request.POST.get('message')
        if ticket_message:
            Message.objects.create(ticket=ticket, message=ticket_message, user=self.request.user)
        return redirect(reverse('ticket_detail', kwargs={'pk': ticket.pk}))

    def test_func(self):
        """
        Checks if the user has permission to view the ticket.
        """
        ticket = self.get_object()
        user = self.request.user
        return (
                user.groups.filter(name='Admin').exists() or
                user.is_superuser or
                (user.groups.filter(name="support").exists() and ticket.assigned_to == user) or
                user == ticket.user
        )


class TicketDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    """
    A view to handle the deletion of a ticket.
    """
    model = Ticket
    template_name = 'tickets/ticket_delete.html'
    success_url = reverse_lazy('tickets_list')

    def test_func(self):
        """
        Only admins and superusers can delete a ticket.
        """
        user = self.request.user
        return user.groups.filter(name='Admin').exists() or user.is_superuser


class TicketAcceptView(UserPassesTestMixin, LoginRequiredMixin, generic.View):
    """
    A view to handle a support user accepting a ticket.
    This has been improved to prevent double-acceptance.
    """

    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=self.kwargs['pk'])

        # Check if the ticket is already assigned
        if ticket.assigned_to:
            messages.error(request, f"Ticket #{ticket.pk} is already assigned to {ticket.assigned_to.username}.")
            return redirect(reverse('tickets_list'))

        ticket.status = 'Pending'
        ticket.assigned_to = self.request.user
        ticket.accepted_at = timezone.now()
        ticket.save()
        messages.success(request, f"Ticket #{ticket.pk} has been successfully assigned to you.")
        return redirect(reverse('ticket_detail', kwargs={'pk': self.kwargs['pk']}))

    def test_func(self):
        """
        Checks if the user has permission to accept a ticket.
        """
        user = self.request.user
        return user.groups.filter(name='support').exists() or user.is_superuser or user.groups.filter(
            name='Admin').exists()


class TicketCloseView(UserPassesTestMixin, LoginRequiredMixin, generic.View):
    """
    A view to handle the closing of a ticket.
    """

    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=self.kwargs['pk'])
        ticket.status = 'Closed'
        ticket.closed_by = self.request.user
        ticket.closed_at = timezone.now()
        ticket.save()
        messages.success(request, f"Ticket #{ticket.pk} has been closed.")
        return redirect(reverse('tickets_list'))

    def test_func(self):
        """
        Checks if the user has permission to close a ticket.
        """
        user = self.request.user
        return user.groups.filter(name='Admin').exists() or user.is_superuser or user.groups.filter(
            name='support').exists()
