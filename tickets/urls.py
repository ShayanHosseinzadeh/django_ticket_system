from django.urls import path

from tickets import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.TicketCreateView.as_view(), name='create_ticket'),
    path('tickets/', views.TicketListView.as_view(), name='tickets_list'),
    path('ticket/<int:pk>', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/<int:pk>/delete', views.TicketDeleteView.as_view(), name='ticket_delete'),
    path('ticket/<int:pk>/accept', views.TicketAcceptView.as_view(), name='ticket_accept'),
    path('ticket/<int:pk>/close', views.TicketCloseView.as_view(), name='ticket_close'),
]