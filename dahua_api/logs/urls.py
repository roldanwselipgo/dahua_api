from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import LogsView
logs_patterns = ([
    path('logs/', login_required(LogsView.as_view()), name='logs'),

], 'logs')


