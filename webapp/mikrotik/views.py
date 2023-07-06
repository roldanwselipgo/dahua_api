from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
import time

from .models import Mikrotik
import pandas as pd

#Download file
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes, os
from celery.result import ResultSet
from celery.result import allow_join_result

from datetime import datetime, timedelta
from django.http import FileResponse
# Create your views here.
class MikrotikListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Mikrotik
    # Handle POST GTTP requests
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        return context
    
    def downloadFile(self, name = "status_file.csv"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename=name
        filepath = base_dir + '/Files/' + filename
        filename=os.path.basename(filepath)
        print(filepath,"f,",filename)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(name,'rb'),chunk_size),
            content_type=mimetypes.guess_type(name)[0])
        response['Content-Length'] = os.path.getsize(name)
        response['Content-Disposition'] = f"Attachment;filename={filename}"
        return response

    def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        #if form.is_valid():
        if self.request.method == "POST":
            # <process form cleaned data>
            if self.request.POST.get("ip",""):
                #--- Insertar camaras de archivo csv 
                ip = str(self.request.POST.get("ip",""))
                user = self.request.POST.get("user","")
                print("ipppp",ip,user)
                if "saka" in ip:
                    return redirect(reverse('mikrotik:mikrotiks')+"?sisako")
                else:
                    return redirect(reverse('mikrotik:mikrotiks')+"?nosako")

            elif self.request.POST.get("port",""):
                f = open('status_file.csv','w+')  
                f.write("")
                f.close()
            
                print("Post method")
                file = self.request.FILES['file']
                port = self.request.POST.get("port","")

                print(file, type(file),port)
                df = pd.read_csv(file, delimiter=',')

                results = []

                #[ results.append(tasks.ip_scanner.delay(f"{row[1]}",int(port),row[0])) for row in df.values]
                [ results.append(tasks.port_scanner.delay(f"{row[1]}",int(port),row[0])) for row in df.values]
                
                while len(results):
                    for i,task in enumerate(results):
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
            
            #response = self.downloadFile()
            return HttpResponse('/success/')
            return response
