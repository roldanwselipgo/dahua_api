from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.admin.models import LogEntry


# Create your views here.
class HomeView(TemplateView):
    logs = LogEntry.objects.all()[:5]
    print("Logs...",logs)
    template_name = "core/home.html"


