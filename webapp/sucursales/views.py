from django.shortcuts import render
from .models import Sucursal,Camera
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from core.dahuaClasses.dahua_class import Dahua
#from core.db import BDBDatabase
from procedures.Vrec.BDB_dbClass import BDBDatabase

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
from datetime import datetime, timedelta

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
        #sucursales=S.objects.using('bdb').filter(sucursal=1104)
        #sucursales=DireccionamientoPrv.objects.using('bdb')[:12]
        data=[]

        '''
        #Consultar segmentos de un dia dahua
        day="2023-04-12"
        starttime = f"{day}%2000:00:00"
        endtime = f"{day}%2023:00:00"
        print("...",starttime,endtime)
        if 1:
            dvr = Dahua("192.168.228.18", 80, "admin", "Elipgo$123")
            by_channels = []
            dvr.MediaFindFileCreate() 
            if 1:
                rsp = dvr.MediaFindFile(-1, starttime, endtime)
                var = 2
                segmentos = []
                while (var):
                    rdict = dvr.MediaFindNextFile(100)
                    if rdict!=-1:
                        for i in range(0,100):
                            channel = rdict[f'items[{i}].Channel']  if f'items[{i}].Channel' in rdict else ""
                            starttime = rdict[f'items[{i}].StartTime']  if f'items[{i}].StartTime' in rdict else ""
                            endtime = rdict[f'items[{i}].EndTime']  if f'items[{i}].EndTime' in rdict else ""
                            if channel and starttime and endtime:
                                segmentos.append((channel,starttime,endtime))
                                print(channel,starttime,endtime)
                    else:
                        var = 0
        #print(segmentos)
        print("count:",len(segmentos))
        return context
        '''
        
        

        """
        #----------------------- Insertar segmentos de video desde CSV file  -----------------------
        bdb   = BDBDatabase() 
        bdb.open_connection()
        with open('result_segmentos.csv') as f:
            lines = f.readlines()
            for line in lines:
                line=line.strip()
                df = line.split(",")
                #print(df[0],df[1],df[2],df[3],df[4])
                bdb.lock.acquire()
                mycursor = bdb.connection.cursor()
                mycursor.execute(f"INSERT INTO segmento_video (sucursal,ip,channel, starttime,endtime) VALUES ({df[0]}, '{df[1]}',{int(df[2])},'{df[3]}','{df[4]}');")
                bdb.connection.commit()
                mycursor.close()
                bdb.lock.release()

        bdb.close_connection()
        #return context
        #----------------------- Insertar segmentos de video desde CSV file  -----------------------
        
        
        
        
        #----------------------- Buscar e insertar segmentos de video perdidos  -----------------------
        bdb   = BDBDatabase() 
        bdb.open_connection()
        bdb.lock.acquire()
        mycursor = bdb.connection.cursor()
        mycursor.execute(f"SELECT distinct * FROM bdb.segmento_video ORDER BY sucursal DESC, channel, starttime;")
        result = mycursor.fetchall()
        #Today dates
        today = datetime.now() 
        today = today - timedelta(days=1)
        #today = datetime.strptime("2023-04-16", "%Y-%m-%d") 
        yesterday = today - timedelta(days=1)
        today.strftime('%Y-%m-%d')
        yesterday.strftime('%Y-%m-%d')
        today = str(today.date())
        yesterday = str(yesterday.date())


        count = 0
        perdidas = 0
        fin_del_video = 0
        channel_tmp = -1
        endtime_tmp = datetime.strptime(f"{today} 23:00:00", "%Y-%m-%d %H:%M:%S")
        sucursal_tmp = 0
        j = 0
        h = 0

        
        if result:
            for res in result:
                #print(res[0],res[1],res[2],res[3], res[4])
                #diff = res[4] - res[3]
                #segundos = diff / timedelta(seconds=1)
                #if segundos > 3901:
                #print("Actual",res[3],res[4])
                #------------------------Verificar que el primer registro empieze a las 00:00:00 o similar
                
                if channel_tmp != int(res[2]):
                    channel_tmp = int(res[2])
                    
                    
                    #print(j,channel_tmp,res)
                    #if  res[3],res[4] # if res[3] between 2023-04-11 23:00 and 2023-04-12 01:00:00
                
                    b = datetime.strptime(f"{yesterday} 22:59:00", "%Y-%m-%d %H:%M:%S")
                    c = datetime.strptime(f"{today} 01:00:00", "%Y-%m-%d %H:%M:%S")
                    if b < res[3] < c:
                        pass
                    else:
                        j=j+1
                        print(res[0],res[1],res[2],res[3],res[4],j)
                        diff =  res[3] - b
                        segundos = diff / timedelta(seconds=1)
                        mins = segundos / 60
                        mycursor.execute(f"INSERT INTO segmento_video2 (sucursal,ip,channel, starttime, endtime, diff) VALUES ({res[0]}, '{res[1]}',{int(res[2])},'{b}','{res[3]}','{mins}');")
                        bdb.connection.commit()
                
                #------------------------Verificar que el ultimo registro termine a las 23:00:00 o similar
                    b = datetime.strptime(f"{today} 22:30:00", "%Y-%m-%d %H:%M:%S")
                    c = datetime.strptime(f"{today} 23:59:00", "%Y-%m-%d %H:%M:%S")
                    if b < endtime_tmp < c:
                        pass
                    else:
                        h=h+1
                        print(res[0],res[1],res[2],res[3],res[4],"h",h,endtime_tmp, sucursal_tmp)
                        diff =  c - endtime_tmp
                        segundos = diff / timedelta(seconds=1)
                        mins = segundos / 60
                        mycursor.execute(f"INSERT INTO segmento_video2 (sucursal,ip,channel, starttime, endtime, diff) VALUES ({res[0]}, '{res[1]}',{int(res[2])},'{endtime_tmp}','{c}','{mins}');")
                        bdb.connection.commit()
                        
                        
                endtime_tmp = res[4]
                sucursal_tmp = res[0]
                
                
                if (fin_del_video != res[3]) and count: # Si fin del video anterior es diferente al inicio del video actual, hay perdida de video
                    diff =  res[3] - fin_del_video
                    segundos = diff / timedelta(seconds=1)
                    mins = segundos / 60
                    if mins>1:
                        mycursor.execute(f"INSERT INTO segmento_video2 (sucursal,ip,channel, starttime, endtime, diff) VALUES ({res[0]}, '{res[1]}',{int(res[2])},'{fin_del_video}','{res[3]}','{mins}');")
                        bdb.connection.commit()
                        perdidas = perdidas + 1
                        print(res[3],res[4],fin_del_video,segundos,perdidas)
                fin_del_video = res[4]
                print("Fin del anterior",fin_del_video)
                
                count = count + 1

            print(count)

        else:
            print("Err...")
            pass
        mycursor.close()
        bdb.lock.release()
        bdb.close_connection()
        return context
        """


        

        """
        #Comparativo con nuevo direccionamiento
        df = pd.read_csv('nuevoDirec.csv', delimiter=',')
        old = []
        news = []
        for row in df.values:
            print(row[0],row[1])
            sucursal=Direccionamiento.objects.using('bdb').filter(sucursal=row[0],xvr=row[1])
            if sucursal:
                old.append((row[0],row[1]))
            else:
                news.append((row[0],row[1]))
        print("\n\nOld vs news",len(old),len(news))
        for new in news:
            print(new[0],new[1])
        """
        
    
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
        
        dvr = Dahua("10.200.3.20", 80, "admin", "Elipgo$123")
        #dvr = Dahua("189.146.107.106", 8401, "admin", "Elipgo$123")
        
        dict_data={}
        dict_data['sucursal']="102"
        dict_data['direccion']="pumas.cantera1.elipgodns.com"
        data.append(dict_data)
        
        """dict_data={}
        dict_data['sucursal']="101"
        dict_data['direccion']="cantera1.auditorio.elipgodns.com"
        data.append(dict_data)
        
        dict_data={}
        dict_data['sucursal']="103"
        dict_data['direccion']="cantera.equipo.elipgodns.com"
        data.append(dict_data)
        dict_data={}
        dict_data['sucursal']="104"
        dict_data['direccion']="pumas.cantera2.elipgodns.com"
        data.append(dict_data)
        dict_data={}
        dict_data['sucursal']="105"
        dict_data['direccion']="pumas.acceso.elipgodns.com"
        data.append(dict_data)"""
        

        '''
        for sucursal in sucursales:
            dict_data={}
            direccion_dvr=Direccionamiento.objects.using('bdb').filter(sucursal=sucursal.sucursal).first()
            #direccion=CamarasPrv.objects.using('bdb').filter(sucursal=sucursal).first()
            print(sucursal.sucursal,len(sucursales))
            direccion=1
            #direccion_dvr=None
            if direccion_dvr.xvr :
                print(direccion_dvr.xvr)

                dict_data['sucursal']=sucursal.sucursal
                dict_data['direccion']=direccion_dvr.xvr
                
                #dict_data['sucursal']=sucursal.xvr
                #dict_data['direccion']=sucursal.cam1
                data.append(dict_data)
        '''   



        task_queue = []
        print("task_queue:", task_queue)   
        for sucursal in data:
            #---------- Conexion a device -------------
            suc = sucursal['sucursal']
            host = sucursal['direccion']
            #port = 80
            port = 8009
            user = "admin"
            password = "Elipgo$123"
            #host="192.168.226.114"
            task=get_sucursal_info_task.delay(host,port,user,password,suc)
            print("Task added: ", task)
            task_queue.append((task,host,suc))

        
        sucursales_result=[]
        sucursales_succes_count = 0
        while len(task_queue):
            for i,task in enumerate(task_queue):
                #print("Scanning in: ", i)
                #if task[0].ready():
                time.sleep(.5)
                print(f"result : {task[0].state} state <--")
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
        file2 = open('info_solo_sucursales.csv','a+')  
        for sucursal in sucursales_result:
            #sucursal = sorted(sucursal, key = sucursal['sucursal'])
            try:
                file2.write(f"{sucursal['sucursal']},{sucursal['direccion']},{sucursal['type']},{sucursal['serial']}")      
            except:
                file2.write(f"{sucursal['sucursal']},{sucursal['direccion']}, '', ''")   
            file2.write("\n")    

            for camera in sucursal['cameras_info']:
                try:
                    file.write(f"{sucursal['sucursal']},{sucursal['direccion']},{sucursal['type']},{sucursal['serial']}, {camera[0]}, {camera[1]}, {camera[2]}, {camera[3]}, {camera[4]}, {camera[5]}, {camera[6]}, {camera[7]}, {camera[8]}, {camera[9]}, {camera[10]}")      
                except:
                    file.write(f"{sucursal['sucursal']},{sucursal['direccion']},{sucursal['type']},{sucursal['serial']}, '', '', '', ''")      

                file.write("\n")      
        
        file.close()
        file2.close()
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
