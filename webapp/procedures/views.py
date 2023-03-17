from django.shortcuts import render

from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
#from django.shortcuts import render, redirect


from procedures import tasks
import time
from .models import Procedure
from .Vrec.XVR import XVR 
import pandas as pd
#Download file
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes, os
from celery.result import ResultSet
from celery.result import allow_join_result

# Create your views here.


class ProceduresListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Procedure
    # Handle POST GTTP requests
    def downloadFile(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename="status_file.csv"
        filepath = base_dir + '/Files/' + filename
        filename=os.path.basename(filepath)
        print(filepath,"f,",filename)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open('status_file.csv','rb'),chunk_size),
            content_type=mimetypes.guess_type('status_file.csv')[0])
        response['Content-Length'] = os.path.getsize('status_file.csv')
        response['Content-Disposition'] = f"Attachment;filename={filename}"
        return response

    def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        #if form.is_valid():
        if self.request.method == "POST":
            # <process form cleaned data>
            if 1:
                f = open('status_file.csv','w+')  
                f.write("")
                f.close()
            
                print("Post method")
                file = self.request.FILES['file']
                port = self.request.POST.get("port","")

                print(file, type(file),port)
                df = pd.read_csv(file, delimiter=',')
                #df = pd.read_csv(file)
                #print(df.values[0])
        # Wait for the tasks to finish 
                results = []
                [ results.append(tasks.port_scanner.delay(f"{row[0]}",int(port))) for row in df.values]
                
                while len(results):
                    for i,task in enumerate(results):
                        #print("Scanning in: ", i)
                        #if task[0].ready():
                        if task.state == "SUCCESS" or task.state=="FAILURE":
                            print(f"Tarea {task} terminada")
                            try:
                                with allow_join_result():
                                    result = task.get()
                                #print("Resultado de tarea: ", result)
                                results.remove(task)
                                print("\nlen results:", len(results))
                            except Exception as e: 
                                print(f"Err en {task}: ", e)
                                results.remove(task)
                                print("len results:", len(results))
                                break
                            finally:
                                break

            else:
                return HttpResponse('/format file error/')
            
            response = self.downloadFile()
            #return HttpResponse('/success/')
            return response


                #for l in list_of_csv:
                    #print(l)
        

    
    def get_queryset(self):
        #if self.request.method == "POST":
        procedures=Procedure.objects.all()
        return procedures


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        return context

    

def update_sucursal_cameras_status(request):
    tasks.usucs()
    return HttpResponse("Success "+str("."), content_type='text/plain')


def update_one_lost(request):
    tasks.update_one()
    return HttpResponse("Success video lost "+str("."), content_type='text/plain')

def summary(request):
    tasks.summary()
    return HttpResponse("Success summary " + str("."), content_type='text/plain')

  
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
    
    