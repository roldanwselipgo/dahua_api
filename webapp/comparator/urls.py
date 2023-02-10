from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import SitioBListView
comparator_patterns = ([
    path('compare/', login_required(SitioBListView.as_view()), name='compare'),

], 'comparator')


