from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import TicketForm
from .models import Ticket, Message


class IndexView(generic.TemplateView):
    template_name = 'tickets/index.html'


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'tickets/createticket.html'
    form_class = TicketForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TicketCreateView, self).form_valid(form)


class TicketListView(LoginRequiredMixin, generic.ListView):
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='Admin').exists() or self.request.user.is_superuser:
            context['open_tickets'] = Ticket.objects.filter(status='Open')
            context['pending_tickets'] = Ticket.objects.filter(status='Pending')
            context['closed_tickets'] = Ticket.objects.filter(status='Closed')
            context['role'] = [role.name for role in self.request.user.groups.all()]

        elif self.request.user.groups.filter(name='support').exists():
            context['open_tickets'] = Ticket.objects.filter(status='Open')
            context['pending_tickets'] = Ticket.objects.filter(Q(status='Pending') | Q(assigned_to=self.request.user))
            context['closed_tickets'] = Ticket.objects.filter(
                Q(status='Closed') & Q(user=self.request.user) | Q(assigned_to=self.request.user))
            context['role'] = [role.name for role in self.request.user.groups.all()]

        else:
            context['open_tickets'] = Ticket.objects.filter(Q(status='Open') & Q(user=self.request.user))
            context['pending_tickets'] = Ticket.objects.filter(Q(status='Pending') & Q(user=self.request.user))
            context['closed_tickets'] = Ticket.objects.filter(Q(status='Closed') & Q(user=self.request.user))
            context['role'] = [role.name for role in self.request.user.groups.all()]

        return context


class TicketDetailView(UserPassesTestMixin, LoginRequiredMixin, generic.DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(ticket=self.get_object().id)
        return context

    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket_message = request.POST.get('message')
        if ticket_message:
            Message.objects.create(ticket=ticket, message=ticket_message, user=self.request.user)
        return redirect(reverse('ticket_detail', kwargs={'pk': ticket.pk}))

    def test_func(self):
        ticket = self.get_object()
        user = self.request.user
        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            return True
        elif user.groups.filter(name="support").exists() and ticket.assigned_to == user:
            return True
        elif user == ticket.user:
            return True
        return False


class TicketDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_delete.html'
    success_url = reverse_lazy('tickets_list')

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists() or self.request.user.is_superuser


class TicketAcceptView(UserPassesTestMixin, LoginRequiredMixin, generic.View):
    model = Ticket

    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=self.kwargs['pk'])
        ticket.status = 'Pending'
        ticket.assigned_to = self.request.user
        ticket.accepted_at = datetime.now()
        ticket.save()
        return redirect(reverse('ticket_detail', kwargs={'pk': self.kwargs['pk']}))

    def test_func(self):
        return self.request.user.groups.filter(name='support').exists() or self.request.user.groups.filter(
            name='Admin').exists() or self.request.user.is_superuser


class TicketCloseView(UserPassesTestMixin, LoginRequiredMixin, generic.View):
    model = Ticket

    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=self.kwargs['pk'])
        ticket.status = 'Closed'
        ticket.closed_by = self.request.user
        ticket.closed_at = datetime.now()
        ticket.save()
        return redirect(reverse('tickets_list'))

    def test_func(self):
        return self.request.user.groups.filter(
            name='Admin').exists() or self.request.user.is_superuser or self.request.user.groups.filter(
            name='support').exists()
