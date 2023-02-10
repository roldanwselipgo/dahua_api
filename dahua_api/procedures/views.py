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
    """xvr = XVR()
    task_queue = []

    for sucursal in xvr.XVRIP[:10]:
        print("Sucursal: ",sucursal)
        task = tasks.update_sucursal_cameras_status.delay(sucursal)
        task_queue.append(task)"""
    tasks.usucs()

    return HttpResponse("Success "+str("."), content_type='text/plain')

"""
def update_sucursal_cameras(request):
    tasks.task_video_lost()
    return HttpResponse("Success video lost "+str("."), content_type='text/plain')


    # start_time = time.time()
    # try:
        
    #     rs = ResultSet([update_sucursal_cameras_task.delay(address) for address in xvr.XVRIP])
    #     rs.get()
    # except:
    #     pass
    # end_time = time.time()
    # print("CelerySquirrel:", end_time - start_time)
    # return str(end_time - start_time)
"""



    
def update_lost(request):
    tasks.task_video_lost()
    """xvr = XVR()
    task_queue = []
    xvr.truncate_table('camara_video_lost')
    for sucursal in xvr.XVRIP[:100]:
        print("Sucursal: ",sucursal)
        task = tasks.update_sucursal_cameras.delay(sucursal)
        task_queue.append((task,sucursal))
    
    print("len task_queue:", len(task_queue))
    while len(task_queue):
        for i,task in enumerate(task_queue):
            #print("Scanning in: ", i)
            if task[0].ready():
                print(f"Tarea {task} terminada")
                try:
                    result = task[0].get()
                    #print("Resultado de tarea: ", result)
                    task_queue.remove(task)
                    print("\nlen task_queue:", len(task_queue))
                except Exception as e: 
                    print(f"Err en {task}: ", e)
                    task_queue.remove(task)
                    print("len task_queue:", len(task_queue))
                    break
                finally:
                    #print(">>>>>>>>")
                    #print(">>>>>>>>")
                    #print(">>>>>>>", result)
                    xvr.update_video_lost(result)
                    break"""
    return HttpResponse("Success video lost "+str("."), content_type='text/plain')
    
    