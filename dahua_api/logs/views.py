from django.shortcuts import render
from django.contrib.admin.models import LogEntry
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy

# Create your views here.

class LogsView(TemplateView):
    template_name = "logs/logentry_list.html"
    def get_queryset(self):
        #for sitio in logs:
        #    print(">", sitio)
        return logs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logs=LogEntry.objects.filter()[:10]
        #logs=LogEntry.objects.filter(action_flag=2)[100:]
        context['logs_list'] = logs
        return context
