from django.shortcuts import render

from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View



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

from .Vrec.mysqlmodels.models import Sucursal as S
from .Vrec.mysqlmodels.models import Direccionamiento
from procedures.Vrec.BDB_dbClass import BDBDatabase
from datetime import datetime, timedelta
from django.http import FileResponse



# Create your views here.


class ProceduresListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Procedure
    # Handle POST GTTP requests
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
            if self.request.POST.get("opcion",""):
                #--- Insertar camaras de archivo csv 
                df = pd.read_csv('1334_info_camaras.csv', index_col=0)
                df = df.to_dict(orient='record')
                # Show dataframe
                d = 0
                bdb   = BDBDatabase() 
                bdb.open_connection()
                for data in df:
                    if len(str(data['a']))>2 and len(data['f'])>2:
                    #if 1 :
                        d = d+1
                        print(data['a'], data['f'], data['g'], data['h'], int(data['p']))

                        bdb.lock.acquire()
                        mycursor = bdb.connection.cursor()

                        mycursor.execute(f"INSERT INTO dispositivo (sucursal, tipo_id, numero_disp,ip,puerto,usuario,password,serie,modelo) VALUES ({data['a']}, 6,{int(data['p'])}, '{data['f']}',80,'admin','Elipgo$123','{data['g']}','{data['h']}');")
                        bdb.connection.commit()
                        #print(myresult)
                        mycursor.close()
                        bdb.lock.release()

                print(d)
                bdb.close_connection()

                return HttpResponse(f'/{d}/')

                


                columna = "SINCRO"
                #columna = "XVR"
                print("Post method")
                file = self.request.FILES['file']
                #df = pd.read_csv(file, delimiter=',')
                #file="Direccionamiento_BDB_2022_csv.csv"
                csv_data_df = pd.read_csv(file)
                df = csv_data_df.to_dict(orient='record')

                bdb   = BDBDatabase() 
                bdb.open_connection()
                index=0

                # ------------ Actualizar o crear sucursal
                cont = 0
                sucs = []
                for data in df:
                    print(data['CENTRO DE COSTOS'],data['SINCRO'])
                    bdb.lock.acquire()
                    mycursor = bdb.connection.cursor()
                    mycursor.execute(f"SELECT * FROM sucursal where sucursal={data['CENTRO DE COSTOS']} order by sucursal desc")
                    result = mycursor.fetchone()
                    if result:
                        print("Toca update")
                    else:
                        cont = cont + 1
                        sucs.append(data['CENTRO DE COSTOS'])
                        #Crear sucursal si no existe
                        mycursor.execute(f"INSERT INTO sucursal (sucursal,fase,implementacion,status) VALUES ({data['CENTRO DE COSTOS']},4,'Entregada','Desconocido');")
                        bdb.connection.commit()
                    mycursor.close()
                    bdb.lock.release()
                print("Conteo",cont,sucs) 
                # Conteo 150 [1107, 1108, 1139, 1271, 1330, 1390, 1395, 1525, 1580, 1591, 1598, 1615, 1645, 1654, 1663, 1678, 1680, 1738, 1748, 1754, 1829, 1856, 1866, 1882, 1958, 1983, 1997, 1998, 2016, 2018, 2024, 2032, 2051, 2061, 2076, 2079, 2081, 2085, 2104, 2111, 2136, 2139, 2143, 2144, 2146, 2152, 2178, 2179, 2195, 2208, 2215, 2218, 2220, 2228, 2231, 2234, 2252, 2253, 2254, 2263, 2273, 2307, 2322, 2331, 2338, 2400, 2412, 2415, 2420, 2421, 2424, 2425, 2438, 2447, 2449, 2453, 2460, 2478, 2500, 2501, 2533, 2540, 2551, 2557, 2558, 2559, 2561, 2569, 2571, 2574, 2577, 2578, 2579, 2585, 2587, 2592, 2599, 2605, 2606, 2607, 2610, 2611, 2617, 2620, 2624, 2625, 2626, 2627, 2632, 2634, 2640, 2642, 2643, 2645, 2656, 2674, 2682, 2689, 2692, 2727, 2728, 2729, 2731, 2743, 2756, 2764, 2769, 2771, 2773, 2776, 2777, 2778, 2792, 2799, 2804, 2814, 2832, 2863, 2873, 2876, 2884, 2886, 2893, 2914, 2922, 2925, 2939, 2943, 2959, 2980]
                 # ------------ Actualizar o crear direccionamiento
                cont = 0
                sucs = []
                for data in df:
                    print(data['CENTRO DE COSTOS'],data['SINCRO'])
                    bdb.lock.acquire()
                    mycursor = bdb.connection.cursor()
                    mycursor.execute(f"SELECT * FROM direccionamiento where sucursal={data['CENTRO DE COSTOS']} order by sucursal desc")
                    result = mycursor.fetchone()
                    if result:
                        #mycursor.execute(f"UPDATE INTO direccionamiento (sucursal,gateway,xvr,xvr_port,xvr_user,xvr_password,alarma,control_acceso,syncroback,switch) \
                        print("Update direccionamiento")
                        mycursor.execute(f"UPDATE direccionamiento SET gateway='{data['GW']}',xvr='{data['XVR']}',xvr_port=80, \
                                         xvr_user='root',xvr_password='root',alarma='{data['ALARMA']}',control_acceso='{data['CONTROL DE ACCESO']}',syncroback='{data['SINCRO']}',switch='{data['SEGURIDAD']}' where sucursal='{data['CENTRO DE COSTOS']}';")
                        #VALUES ('{data['CENTRO DE COSTOS']}','{data['GW']}','{data['XVR']}',80,'root','root','{data['ALARMA']}','{data['CONTROL DE ACCESO']}','{data['SINCRO']}','{data['SEGURIDAD']}');")
                        bdb.connection.commit()
                    else:
                        cont = cont + 1
                        sucs.append(data['CENTRO DE COSTOS'])
                        #Crear direccionamiento si no existe
                        mycursor.execute(f"INSERT INTO direccionamiento (sucursal,gateway,xvr,xvr_port,xvr_user,xvr_password,alarma,control_acceso,syncroback,switch) \
                                         VALUES ('{data['CENTRO DE COSTOS']}','{data['GW']}','{data['XVR']}',80,'root','root','{data['ALARMA']}','{data['CONTROL DE ACCESO']}','{data['SINCRO']}','{data['SEGURIDAD']}');")
                        bdb.connection.commit()
                    mycursor.close()
                    bdb.lock.release()
                print("Conteo",cont,sucs) 
                #bdb.close_connection()
                #return HttpResponse(f'/2 {cont}/')

                
                dispositivos=Direccionamiento.objects.using('bdb').filter(sucursal__gte=1104)
                
                for dispositivo in dispositivos:
                    print(dispositivo)
                    print("XVRRR",dispositivo.xvr)
                
                #for data in XVRs:
                    print(str(data[columna]))
                    index=index+1
                    bdb.lock.acquire()
                    mycursor = bdb.connection.cursor()
                    mycursor.execute(f"INSERT INTO dispositivo (sucursal, tipo_id, numero_disp,ip) VALUES ({dispositivo.sucursal}, 7,{index}, '{dispositivo.alarma}');")
                    bdb.connection.commit()
                    mycursor.execute(f"INSERT INTO dispositivo (sucursal, tipo_id, numero_disp,ip) VALUES ({dispositivo.sucursal}, 8,{index}, '{dispositivo.control_acceso}');")
                    bdb.connection.commit()
                    mycursor.execute(f"INSERT INTO dispositivo (sucursal, tipo_id, numero_disp,ip) VALUES ({dispositivo.sucursal}, 2,{index}, '{dispositivo.switch}');")
                    bdb.connection.commit()
                    mycursor.execute(f"INSERT INTO dispositivo (sucursal, tipo_id, numero_disp,ip) VALUES ({dispositivo.sucursal}, 1,{index}, '{dispositivo.gateway}');")
                    bdb.connection.commit()
                    mycursor.execute(f"INSERT INTO dispositivo (sucursal, tipo_id, numero_disp,ip) VALUES ({dispositivo.sucursal}, 5,{index}, '{dispositivo.syncroback}');")
                    bdb.connection.commit()
                    mycursor.execute(f"INSERT INTO dispositivo (sucursal, tipo_id, numero_disp,ip,puerto,usuario,password) VALUES ({dispositivo.sucursal}, 3,{index}, '{dispositivo.xvr}',80,'admin','Elipgo$123');")
                    bdb.connection.commit()
                    #print(myresult)
                    mycursor.close()
                    bdb.lock.release()


                    #Actualizar series y modelos de status_file.csv
                    df = pd.read_csv('info_solo_sucursales.csv', delimiter=',')
                    for row in df.values:
                        bdb.lock.acquire()
                        mycursor = bdb.connection.cursor()
                        mycursor.execute(f"UPDATE dispositivo SET serie='{row[2]}',modelo='{row[3]}' where ip='{row[1]}';")
                        #VALUES ('{data['CENTRO DE COSTOS']}','{data['GW']}','{data['XVR']}',80,'root','root','{data['ALARMA']}','{data['CONTROL DE ACCESO']}','{data['SINCRO']}','{data['SEGURIDAD']}');")
                        bdb.connection.commit()
                        mycursor.close()
                        bdb.lock.release()
                bdb.close_connection()
                
                return HttpResponse('/0/')
            if self.request.POST.get("port",""):
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

                #[ results.append(tasks.ip_scanner.delay(f"{row[1]}",int(port),row[0])) for row in df.values]
                [ results.append(tasks.port_scanner.delay(f"{row[1]}",int(port),row[0])) for row in df.values]
                
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

    

def update_noip_status(request):
    bdb   = BDBDatabase() 
    bdb.open_connection()
    index=0
    # ------------ Actualizar o crear sucursal
    bdb.lock.acquire()
    mycursor = bdb.connection.cursor()
    mycursor.execute(f"SELECT * FROM devices.dvrDevices where port is not null and isConfigured=1 and status=1;")
    sucursales = mycursor.fetchall()
    for sucursal in sucursales:
        print(f"sucursal: {sucursal[0]}")
        tasks.port_scanner.delay(f"{sucursal[0]}",int(8012),100)
    mycursor.close()
    bdb.lock.release()
    bdb.close_connection()
    #[ results.append(tasks.port_scanner.delay(f"{row[1]}",int(port),row[0])) for row in df.values]
    return HttpResponse("Success "+str("."), content_type='text/plain')

def update_sucursal_cameras_status(request):
    tasks.task_cameras_status()
    return HttpResponse("Success "+str("."), content_type='text/plain')


def update_one_lost(request):
    tasks.update_one()
    return HttpResponse("Success video lost "+str("."), content_type='text/plain')

def summary(request):
    tasks.summary()
    return HttpResponse("Success summary " + str("."), content_type='text/plain')


def update_sucursales_status(request):
    results = []
    port = 80
    sucursales=S.objects.using('bdb').exclude(fase=1)
    for sucursal in sucursales:
        dict_data={}
        direccion_dvr=Direccionamiento.objects.using('bdb').filter(sucursal=sucursal.sucursal).first()
        #direccion=CamarasPrv.objects.using('bdb').filter(sucursal=sucursal).first()
        print(sucursal.sucursal,len(sucursales))
        direccion=1
        #direccion_dvr=None
        if direccion_dvr.xvr:
            print(direccion_dvr.xvr)
            results.append(tasks.port_scanner.delay(direccion_dvr.xvr,int(port),sucursal.sucursal))
            #results.append(tasks.ip_scanner.delay(direccion_dvr.xvr,int(port),sucursal.sucursal))
    
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
    return HttpResponse("Success update_sucursales_status " + str("."), content_type='text/plain')


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
    
    
class DescargarArchivoView(View):
    def get(self, request):
        # Ruta al archivo que deseas descargar
        ruta_archivo = '/ruta/al/archivo/archivo.txt'
        
        # Abre el archivo en modo lectura binaria
        with open(ruta_archivo, 'rb') as archivo:
            response = FileResponse(archivo)
            
            # Establece el tipo MIME del archivo
            response['Content-type'] = 'application/octet-stream'
            
            # Establece el encabezado para la descarga del archivo
            response['Content-Disposition'] = 'attachment; filename="archivo.txt"'
            return 2
        
def downloadFile2(self, name = "status_file.csv"):
        time.sleep(20)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_archivo = name
        with open(ruta_archivo, 'rb') as archivo:
            response = FileResponse(archivo)
            
            # Establece el tipo MIME del archivo
            response['Content-type'] = 'application/octet-stream'
            
            # Establece el encabezado para la descarga del archivo
            response['Content-Disposition'] = f'attachment; filename={name}'
            return response
        
def downloadFile(self, name = "result_segmentos_this.csv"):
        time.sleep(20)
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


def update_lost_dahua(request):
    results = []
    port = 80
    sucursales=S.objects.using('bdb').exclude(fase=1)[:1]
    print("Update_lost_dahua")
    
    file = open('result_segmentos.csv','w+')
    file.write("")
    file.close()

    for sucursal in sucursales:
        dict_data={}
        direccion_dvr=Direccionamiento.objects.using('bdb').filter(sucursal=sucursal.sucursal).first()
        #direccion=CamarasPrv.objects.using('bdb').filter(sucursal=sucursal).first()
        print(sucursal.sucursal,len(sucursales))
        direccion=1
        #direccion_dvr=None
        if direccion_dvr.xvr:
            print(direccion_dvr.xvr)
            #Sucursales fija
            results.append(tasks.task_video_lost_dahua.delay('10.200.3.182',int(port),sucursal.sucursal))
            #results.append(tasks.task_video_lost_dahua.delay(direccion_dvr.xvr,int(port),sucursal.sucursal))
            
            #results.append(tasks.ip_scanner.delay(direccion_dvr.xvr,int(port),sucursal.sucursal))
    f = "result_segmentos.csv"
    file = downloadFile(f)
    #return redirect('DescargarArchivoView')
    return file
    return HttpResponse("Success video lost dahua "+str("."), content_type='text/plain')

    """while len(results) > 30:
        for i,task in enumerate(results):
            if task.state == "SUCCESS":
                results.remove(task)
                print("len results:", len(results))
                break
            elif task.state == "FAILURE":
                results.remove(task)
                print("len results:", len(results))
                break"""

    
    #----------------------- Insertar segmentos de video desde CSV file  -----------------------
    bdb   = BDBDatabase() 
    bdb.open_connection()
    bdb.lock.acquire()
    mycursor = bdb.connection.cursor()
    mycursor.execute(f"TRUNCATE segmento_video")
    bdb.connection.commit()
    mycursor.execute(f"TRUNCATE segmento_video2")
    bdb.connection.commit()
    mycursor.close()
    bdb.lock.release()

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
    

    #return HttpResponseRedirect(reverse('sucursal:sucursales'))
    return HttpResponse("Success video lost dahua "+str("."), content_type='text/plain')
    