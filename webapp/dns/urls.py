from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import DNSListView,DNSDetailView,DNSCreateView, DNSUpdateView, DNSDeleteView
dns_patterns = ([
    path('dnss/', login_required(DNSListView.as_view()), name='dnss'),
    path('dns/<int:pk>', login_required(DNSDetailView.as_view()), name='dns'),
    path('dnss/create/', login_required(DNSCreateView.as_view()), name='create'),
    path('dns/update/<int:pk>', login_required(DNSUpdateView.as_view()), name='update'),
    path('dns/delete/<int:pk>', login_required(DNSDeleteView.as_view()), name='delete'),
], 'dns')