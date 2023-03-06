from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomeView

core_patterns = ([
    path('', login_required(HomeView.as_view()), name='home'),
], 'core')