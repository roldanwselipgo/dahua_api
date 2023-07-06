from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import MikrotikListView
mikrotik_patterns = ([
    path('mikrotiks/', MikrotikListView.as_view(), name='mikrotiks'),
    path('mikrotiks/<str:result>', MikrotikListView.as_view(), name='mikrotiks_result'),
], 'mikrotik')