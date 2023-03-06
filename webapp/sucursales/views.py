from django.shortcuts import render
from .models import Sucursal,Camera
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from core.dahuaClasses.dahua_class import Dahua
from core.db import BDBDatabase
from core.dahuaClasses.dahua_config import Config as Conf
from sucursales.tasks import get_sucursal_info_task
import time
from django.http import HttpResponse
import logging
import shutil
from procedures.Vrec.mysqlmodels.models import Sucursal as S
from procedures.Vrec.mysqlmodels.models import Direccionamiento 
from celery.result import allow_join_result

# Create your views here.


class SucursalListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Sucursal
    #def get_queryset(self):
    #    sucursales=Sucursal.objects.all()
    #    return sucursales
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sucursales=S.objects.using('bdb').filter(fase=2)
        data=[]
        for sucursal in sucursales:
            dict_data={}
            direccion=Direccionamiento.objects.using('bdb').filter(sucursal=sucursal.sucursal).first()
            dict_data['sucursal']=sucursal.sucursal
            dict_data['direccion']=direccion.xvr
            data.append(dict_data)

        #union = direcciones.union(sucursales)


        task_queue = []
        print("task_queue:", task_queue)   
        for sucursal in data:
            #---------- Conexion a device -------------
            suc = sucursal['sucursal']
            host = sucursal['direccion']
            port = 80
            user = "admin"
            password = "Elipgo$123"
            task=get_sucursal_info_task.delay(host,port,user,password)
            print("Task added: ", task)
            task_queue.append((task,host,suc))

        
        sucursales_result=[]
        while len(task_queue):
            for i,task in enumerate(task_queue):
                #print("Scanning in: ", i)
                #if task[0].ready():
                #print(f"result : {task[0].state} state <--")
                if task[0].state == "SUCCESS":
                    
                    print(f"Tarea {task} terminada")
                    if 1:
                        with allow_join_result():
                            result = task[0].get()
                            print(f"Result {result} ")
                            dict_result={}
                            if result:
                                if 'type' in result:
                                    
                                    type=result['type']
                                    print(task[1],type)
                                    dict_result['sucursal']=task[2]
                                    dict_result['direccion']=task[1]
                                    dict_result['type']=type
                                    sucursales_result.append(dict_result)
                            else:
                                dict_result['sucursal']=task[2]
                                dict_result['direccion']=task[1]
                                dict_result['type']='None'
                                sucursales_result.append(dict_result)
                        #print("Resultado de tarea: ", result)
                        task_queue.remove(task)
                        print("\nlen task_queue:", len(task_queue))
                        
        context['sucursales']=sucursales_result
        return context

    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sitios = []
        if 0:
            #print("Conection success mysql")
            bd = BDBDatabase()
            vc = Config.objects.filter(id=1).first()
            sitios = bd.GetSitios()
            for sitio in sitios:
                if 0:
                #if len(sitio):
                    proyecto = sitio[0]
                    id_sitio = sitio[1]
                    ip = f"mc{id_sitio}.c5cdmx.elipgodns.com"
                    status = sitio[3]
                    is_alive = sitio[4]
                    last_update = sitio[5]
                    data = {
                        'sitio':id_sitio,
                        'proyecto':proyecto,
                        'ip':ip,
                        'status':status,
                        'is_alive':is_alive,
                        'last_update':last_update,
                        'videoencode_config_id':vc,
                    }
                    print(sitio,len(sitio))
                    print(id_sitio,proyecto,ip,status,is_alive,last_update,vc)
                    #Update_or_create
                    try:
                        item = Sitio.objects.get(sitio=id_sitio)
                    except Sitio.DoesNotExist:
                        Sitio.objects.create(sitio=id_sitio,proyecto=proyecto, ip=ip,
                            status=status,is_alive=is_alive,last_update=last_update,
                            videoencode_config_id=vc)
                    else:
                        item = Sitio.objects.filter(
                            sitio=id_sitio
                        ).update(
                            ip=ip, status=status, is_alive=is_alive,
                            last_update=last_update, videoencode_config_id=vc
                        )
                    print(item)
                    
            context['sitios'] = Sitio.objects.all()
        return context'''


class SucursalDetailView(DetailView):
    ''' Vista encargada de detallar el dispositivo seleccionado '''
    model = Sucursal
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #---------- Conexion a device -------------
        host = self.object.ip
        port = 8011
        user = "admin"
        password = "Elipgo$123"
        dvr = Dahua(host, port, user, password) 
        general = dvr.GetGeneralConfig()
        device_type = dvr.GetDeviceType()
        device_type = device_type['type']  if 'type' in device_type else ""
        hardware_version = dvr.GetHardwareVersion()
        hardware_version = hardware_version['version']  if 'version' in hardware_version else ""
        serial_number = dvr.GetSerialNumber()
        serial_number = serial_number['sn']  if 'sn' in serial_number else ""
        current_time = dvr.GetCurrentTime()
        locales = "device1.obtener_locales_config()"
        di = dvr.GetDeviceInfo() 
        video_encode_settings = dvr.GetMediaEncode() 
        snapshot = dvr.GetSnapshot() 
        print("snap", snapshot.raw)
        print("gral", general)
        if snapshot.status_code == 200:
            #print(video_encode_settings, type(video_encode_settings))
            with open("device/static/device/snapshot.jpg", 'wb') as f:
                snapshot.raw.decode_content = True
                shutil.copyfileobj(snapshot.raw, f) 

        context['general']=general
        context['current_time']=current_time
        context['locales']=locales
        context['device_type']=device_type
        context['serial_number']=serial_number
        context['hardware_version']=hardware_version
        context['video_encode_settings']=video_encode_settings
        return context
