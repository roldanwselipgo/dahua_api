from django.shortcuts import render

from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse


from procedures import tasks
import time
from .models import Procedure
from .Vrec.XVR import XVR 

# Create your views here.


class ProceduresListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Procedure
    def get_queryset(self):
        procedures=Procedure.objects.all()
        return procedures


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        return context

    

def update_sucursal_cameras_status(request):
    xvr = XVR()
    task_queue = []

    for sucursal in xvr.XVRIP[:10]:
        print("Sucursal: ",sucursal)
        task = tasks.update_sucursal_cameras_status.delay(sucursal)
        task_queue.append(task)

    return HttpResponse("Success "+str("."), content_type='text/plain')