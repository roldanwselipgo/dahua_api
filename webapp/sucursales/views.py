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
from procedures.Vrec.mysqlmodels.models import Direccionamiento , DireccionamientoPrv, CamarasPrv
from celery.result import allow_join_result
import pandas as pd

# Create your views here.


class SucursalListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Sucursal
    #def get_queryset(self):
    #    sucursales=Sucursal.objects.all()
    #    return sucursales
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sucursales=S.objects.using('bdb').exclude(fase=1)
        #sucursales=DireccionamientoPrv.objects.using('bdb')[:12]
        data=[]
        """
        
        df = pd.read_csv('sucursales_con_direccionamiento_1.csv')
        #sh = df['GRABADOR'].tolist()
        #print(sh)
        #df = pd.read_csv(file)
        #print(df.values[0])
        # Wait for the tasks to finish 
        results = []
        count_suc = []
        count_new = []
        for row in df.values:
            print("suc: ",row[0])
            suc = Direccionamiento.objects.using('bdb').filter(sucursal=row[0],xvr=row[2],alarma=row[3],control_acceso=row[4],syncroback=row[5]).first()
            #suc = Direccionamiento.objects.using('bdb').filter(sucursal=row[0]).first()
            if suc:
                count_suc.append(row[0])
            else:
                #if row[0]==1138:
                if 1:
                    print("test update:",row[0])
                    #find = Direccionamiento.objects.using('bdb').filter(sucursal=row[0])
                    #updated = find.update(xvr=row[2],xvr_port=80,xvr_user="root",xvr_password="root",alarma=row[3],control_acceso=row[4],syncroback=row[5])
                    #created = Direccionamiento.objects.using('bdb').create(sucursal=row[0],xvr=row[2],xvr_port=80,xvr_user="root",xvr_password="root",alarma=row[3],control_acceso=row[4],syncroback=row[5])
                count_new.append(row[0])

                print("new:", row)
        print("Count_suc",len(count_suc), count_suc)
        print("Count_new",len(count_new),count_new)
        """
        #sucursales = [1401, 2432, 2240, 2246, 2689, 1323, 2761, 2074, 2904, 2048, 2297, 1592, 1737, 1835, 2137, 2419, 1517, 2055, 1674, 2272, 2505, 1630, 2255, 2554, 2567, 2261, 1699, 2906, 1303, 2462, 2747, 1989, 1828, 2210, 2457, 2694]
        for sucursal in sucursales:
            dict_data={}
            direccion_dvr=Direccionamiento.objects.using('bdb').filter(sucursal=sucursal.sucursal).first()
            #direccion=CamarasPrv.objects.using('bdb').filter(sucursal=sucursal).first()
            print(sucursal.sucursal,len(sucursales))
            direccion=1
            #direccion_dvr=None
            if direccion_dvr.xvr:
                print(direccion_dvr.xvr)

                dict_data['sucursal']=sucursal.sucursal
                dict_data['direccion']=direccion_dvr.xvr
                
                
                #dict_data['sucursal']=sucursal.xvr
                #dict_data['direccion']=sucursal.cam1
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
            #host="192.168.226.114"
            task=get_sucursal_info_task.delay(host,port,user,password)
            print("Task added: ", task)
            task_queue.append((task,host,suc))

        
        sucursales_result=[]
        sucursales_succes_count = 0
        while len(task_queue):
            for i,task in enumerate(task_queue):
                #print("Scanning in: ", i)
                #if task[0].ready():
                #print(f"result : {task[0].state} state <--")
                #if task[0].state == "SUCCESS" or task[0].state == "FAILURE":
                if task[0].state == "SUCCESS":
                    
                    print(f"Tarea {task} terminada")
                    if 1:
                        with allow_join_result():
                            result = task[0].get()
                            print(f"Result {result} ")
                            dict_result={}
                            
                            if result:
                                type = result[0]
                                serial_dvr = result[1]
                                cameras_info = result[2]
                                if cameras_info:
                                    dict_result['sucursal']=task[2]
                                    dict_result['direccion']=task[1]
                                    dict_result['type']=type
                                    dict_result['serial']=serial_dvr
                                    dict_result['cameras_info']=cameras_info
                                    sucursales_result.append(dict_result)
                                    sucursales_succes_count = sucursales_succes_count + 1

                            else:
                                dict_result['sucursal']=task[2]
                                dict_result['direccion']=task[1]
                                dict_result['type']='None'
                                dict_result['serial']='None'
                                dict_result['cameras_info']=['']
                                sucursales_result.append(dict_result)
                        #print("Resultado de tarea: ", result)
                        task_queue.remove(task)
                        print("\nlen task_queue:", len(task_queue))
                elif task[0].state == "FAILURE":
                    dict_result={}
                    dict_result['sucursal']=task[2]
                    dict_result['direccion']=task[1]
                    dict_result['type']='None'
                    dict_result['serial']=''
                    dict_result['cameras_info']=['']
                    sucursales_result.append(dict_result)
                    task_queue.remove(task)
                    print("len task_queue:", len(task_queue))
                    break

        file = open('info_sucursales.csv','a+')  
        for sucursal in sucursales_result:
            #sucursal = sorted(sucursal, key = sucursal['sucursal'])
            for camera in sucursal['cameras_info']:
                try:
                    file.write(f"{sucursal['sucursal']},{sucursal['direccion']},{sucursal['type']},{sucursal['serial']}, {camera[0]}, {camera[1]}, {camera[2]}, {camera[3]}, {camera[4]}, {camera[5]}, {camera[6]}, {camera[7]}, {camera[8]}, {camera[9]}, {camera[10]}")      
                except:
                    file.write(f"{sucursal['sucursal']},{sucursal['direccion']},{sucursal['type']},{sucursal['serial']}, '', '', '', ''")      

                file.write("\n")      
        
        file.close()
        context['sucursales']=sucursales_result
        context['sucursales_len']=sucursales_succes_count
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
