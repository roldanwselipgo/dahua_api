# Create your tasks here

from celery import shared_task
import time
from celery.result import allow_join_result
from .models import Procedure
from procedures.Vrec.XVR import XVR 
from procedures.Vrec.BDB_dbClass import BDBDatabase
from procedures.Vrec.VRecWSClient import VRecWSClient
from procedures.Vrec.VRecCamera import ProcessVideoList
import logging
import nmap
import requests
#from procedures.views import update_lost 
from core.dahuaClasses.dahua_class import Dahua
from datetime import date
from datetime import timedelta
import pydig

bdb   = BDBDatabase()


@shared_task(name="ProcessXVRTask")
def ProcessXVR(sucursal):
    logging.info(f"ProcessXVR({sucursal})")

    numeroSuc = sucursal[0]
    vrecHost  = sucursal[1]
    vrecPost  = sucursal[2]
    vrecUser  = sucursal[3]
    vrecPass  = sucursal[4]

    print(f"Procesando Sucursal: {numeroSuc}:'{vrecHost}'")    
    bdb.WriteLog(numeroSuc, "Started")

    vrec = VRecWSClient(vrecHost, port=vrecPost, sucursal=numeroSuc, user=vrecUser, password=vrecPass)
    #print("After Construct")
    if (vrec.exception):
        bdb.WriteLog(numeroSuc, vrec.exception)
        bdb.UpdateStatus(numeroSuc, vrec.exception)
    else:
        bdb.UpdateStatus(numeroSuc, "Online")

    #vrec.GetRepositories()
    #vrec.GetBackupRepository()

    # Obtiene la Lista de Cámaras el Sitio
    #print("Vrec.cliente:", vrec.client)
    if (vrec.client and not vrec.exception):
        bdb.WriteLog(numeroSuc, "CameraList")        
        cameras = vrec.GetCameraList()
        if (cameras):
            for cameraId in cameras:
                bdb.WriteLog(numeroSuc, f"CameraId:{cameraId}")

                camera = vrec.GetCameraData(cameraId)
                #print("CameraDataResponse: ",camera,len(camera))
                if 1:
                    firstDate, lastDate, lost = ProcessVideoList(videoList)

                    camaraInfo = {}
                    camaraInfo['sucursal']       = numeroSuc
                    camaraInfo['camara']         = camera["CameraID"]
                    camaraInfo['nombre']         = camera["Name"]
                    camaraInfo['host']           = camera["Host"]
                    camaraInfo['port']           = camera["PortHTTP"]
                    camaraInfo['sdk']            = camera["SDK"]
                    camaraInfo['user']           = camera["User"]
                    camaraInfo['password']       = camera["Password"]
                    camaraInfo['fps']            = camera["FrameRate"]
                    camaraInfo['status']         = camera["Status"]
                    camaraInfo['enable']         = camera["Enable"]
                    camaraInfo['recycle_mode']   = camera["RecycleMode"]
                    camaraInfo['recycle_status'] = camera["RecycleStatus"]
                    camaraInfo['firstDate']      = str(firstDate)
                    camaraInfo['lastDate']       = str(lastDate)
                    camaraInfo['lost']           = str(lost)


                    videoList = vrec.GetCameraVideoList(cameraId)
                    if (videoList):
                        bdb.WriteLog(numeroSuc, f"VideoList:{cameraId}")
                        #print("VideoList: ", videoList)
                        firstDate, lastDate, lost = ProcessVideoList(videoList)
                        camaraInfo['firstDate']      = str(firstDate)
                        camaraInfo['lastDate']       = str(lastDate)
                        camaraInfo['lost']           = lost

                    #print(camaraInfo)
                    bdb.UpdateCameraRecord(camaraInfo)
                    bdb.UpdateCameraLost(camaraInfo, lost)

    try:
        vrec = None
        bdb.WriteLog(numeroSuc, "Finished")
        print(f"Terminando Sucursal: {numeroSuc}:'{vrecHost}'")
    except:
        bdb.WriteLog(numeroSuc, "Exception")
        print("EXCEPTION")
        


@shared_task(name="ip_scanner")
def ip_scanner(address, port, sucursal):
    timeout=10
    response=1
    i="ok"


    bdb.open_connection()    
    
    if 1:

        if 1:
            nm = nmap.PortScanner()
            nm.scan(hosts=address, arguments='-sP', timeout=30)

            response = nm[address].state()
            print(nm,response)
            if response:
                print(response)

            if response == "up":
                print (address, 'is up!', response)
                file = open('status_file.csv','a+')  
                file.write(f"{sucursal},{address},1\n")
                file.close()
                #bdb.UpdateStatus(sucursal,"Online")
            else:
                print (address, 'is down!', response)
                file = open('status_file.csv','a+')  
                file.write(f"{sucursal},{address},0\n")
                file.close()
                #bdb.UpdateStatus(sucursal,"Sin Acceso")

        else:
            print (i,address, 'unresolve!', response)
            file = open('status_file.csv','a+')  
            file.write(f"{sucursal},{address},2\n")
            file.close()
    bdb.close_connection()
    

@shared_task(name="port_scanner")
def port_scanner(address, port, sucursal):
    timeout=10
    response=1
    i="ok"

    bdb.open_connection()    
    if 1:
        print(f"port_scanner()", flush=True)
        try:
            nm = nmap.PortScanner()
            r = nm.scan(address, str(port), arguments='-Pn  --max-retries 10 --host-timeout 30s')
            print(r)
            response = nm.all_hosts()[0]
            if response:
                host = nm.all_hosts()[0]
                response = nm[f'{host}'].tcp(port)['state']

            if response == "open":
                print (address, 'is up!', response)
                file = open('status_file.csv','a+')  
                file.write(f"{sucursal},{address},1\n")
                file.close()
                bdb.UpdateStatus(sucursal,"Online")
                #Actualizar status NoIp
                #bdb.UpdateStatusNoIp(address,1)
            else:
                print (address, 'is down!', response)
                file = open('status_file.csv','a+')  
                file.write(f"{sucursal},{address},0\n")
                file.close()
                #bdb.UpdateStatus(sucursal,"Sin Acceso")

        except:
            print (i,address, 'unresolve!', response)
            file = open('status_file.csv','a+')  
            file.write(f"{address},2\n")
            file.close()
    bdb.close_connection()
    



@shared_task(name="task_video_lost_dahua", time_limit=180)
def task_video_lost_dahua(host, port, suc):

    today = date.today()
    yesterday = today - timedelta(days = 1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    yesterday = '2023-06-08'
    starttime = f"{yesterday}%2000:00:00"
    endtime = f"{yesterday}%2023:00:00"
    print("...",starttime,endtime)
    #print("Today is: ", today, yesterday, type(today))
    #return 0
    if 1:
        dvr = Dahua(host, port, "admin", "Elipgo$123")
        by_channels = []

        bdb.open_connection()  
        file = open('result_segmentos.csv','a+')

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
                            file.write(f"{suc},{host},{channel},{starttime},{endtime} \n")
                            
                            """
                            #Insertar a base
                            bdb.lock.acquire()
                            mycursor = bdb.connection.cursor()
                            query1=f"SELECT * from segmento_video where sucursal={suc} and ip='{host}' and channel={int(channel)} and starttime='{starttime}' and endtime='{endtime}'"
                            #print(queryStr)
                            result=None
                            if 1:
                                mycursor.execute(query1)
                                result = mycursor.fetchall()
                                print("RESULTTTT", result)
                            else:
                                pass
                            if not result:
                                mycursor.execute(f"INSERT INTO segmento_video (sucursal,ip,channel, starttime,endtime) VALUES ({suc}, '{host}',{int(channel)},'{starttime}','{endtime}');")
                                bdb.connection.commit()
                            mycursor.close()
                            bdb.lock.release()
                            """
                else:
                    var = 0
            by_channels.append(segmentos)
            #print(segmentos)
        #print(by_channels)
        file.close()
        bdb.close_connection() 
        return None
    else:
        return None

@shared_task(name="task_video_lost")
def task_video_lost():
    bdb.open_connection()
    XVRIP = bdb.GetVRecIP()
    xvr = XVR(bdb)
    
    task_queue = []
    #xvr.truncate_table('camara_video_lost')
    for sucursal in XVRIP:
        #if sucursal[0]==101:
        if 1:
            print("Sucursal: ",sucursal)
            task = update_sucursal_cameras.delay(sucursal)
            print("Task added: ", task)
            task_queue.append((task,sucursal))
        #    break
    
    print(">>>>>>TASKS: ", task_queue)
    print("task_queue:", task_queue)
    logging.warning("Init while:")    
    while len(task_queue):
        for i,task in enumerate(task_queue):
            #print("Scanning in: ", i)
            #if task[0].ready():
            #print(f"result : {task[0].state} state <--")
            if task[0].state == "SUCCESS":
                print(f"Tarea {task} terminada")
                try:
                    with allow_join_result():
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
                    """file = open('logslost22.txt','a+') 
                    print(".")
                    print("result",result)
                    if result:   
                        for cameraInfo in result:
                            lost = cameraInfo['lost']
                            for lost_segment in lost:
                                file.write("\n")
                                file.write(f"sucursal:  {cameraInfo['sucursal']} > video_lost:  {lost_segment[0]} , {lost_segment[1]} ")
                    file.close()"""
                    #xvr.update_video_lost(result)
                    break
            elif task[0].state == "FAILURE":
                task_queue.remove(task)
                print("len task_queue:", len(task_queue))
                break
    bdb.close_connection()
    




@shared_task(name="task_camera_status")
def task_camera_status():
    bdb.open_connection()
    XVRIP = bdb.GetVRecIP()
    xvr = XVR(bdb)
    task_queue = []
    #xvr.truncate_table('camara_camera_status')
    for sucursal in XVRIP:
        #if sucursal[0]==101:
        if 1:
            print("Sucursal: ",sucursal)
            task = update_sucursal_cameras.delay(sucursal)
            print("Task added: ", task)
            task_queue.append((task,sucursal))
        #    break
    
    print(">>>>>>TASKS: ", task_queue)
    print("task_queue:", task_queue)
    logging.warning("Init while:")    
    while len(task_queue):
        for i,task in enumerate(task_queue):
            #print("Scanning in: ", i)
            #if task[0].ready():
            #print(f"result : {task[0].state} state <--")
            if task[0].state == "SUCCESS":
                print(f"Tarea {task} terminada")
                try:
                    with allow_join_result():
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
                    """file = open('logslost22.txt','a+') 
                    print(".")
                    print("result",result)
                    if result:   
                        for cameraInfo in result:
                            lost = cameraInfo['lost']
                            for lost_segment in lost:
                                file.write("\n")
                                file.write(f"sucursal:  {cameraInfo['sucursal']} > camera_status:  {lost_segment[0]} , {lost_segment[1]} ")
                    file.close()"""
                    #xvr.update_video_lost(result)
                    break
            elif task[0].state == "FAILURE":
                task_queue.remove(task)
                print("len task_queue:", len(task_queue))
                break
    bdb.close_connection()


@shared_task(name="update_sucursal_cameras", time_limit=80)
def update_sucursal_cameras(sucursal):
    start_time = time.time()
    if 1:
        bdb.open_connection()
        xvr = XVR(bdb)
        cameraInfo = xvr.update_sucursal_cameras(sucursal) 
        bdb.close_connection()

    end_time = time.time()
    print("time:", end_time - start_time)
    return cameraInfo

@shared_task(name="update_one", time_limit=32)
def update_one():
    bdb.open_connection()
    XVRIP = bdb.GetVRecIP()
    xvr = XVR(bdb)
    for sucursal in XVRIP:
        if sucursal[0]==101:
            xvr.update_sucursal_cameras(sucursal)
    bdb.close_connection()
    return 'Sucursal procesada'

@shared_task(name="summary", time_limit=32)
def summary():
    print("summary()")
    bdb.open_connection()
    print("bdopen()")
    summary = bdb.GetSummaryDahua()
    summary = bdb.GetSummary()
    bdb.close_connection()
    return 'Sucursal procesada'

@shared_task(name="video_lost")
def video_lost():
    response = requests.get('http://192.168.60.199:8000/camera_video_lost/')
    return response

@shared_task(name="test", time_limit=32)
def test():
    a = 2
    return a*a


"""

@shared_task(name="celery.update_sucursal_cameras_status_task", time_limit=32)
def update_sucursal_cameras_status_task(sucursal):
    return xvr.update_sucursal_cameras_status(sucursal)

@shared_task(name="celery.update_sucursal_cameras_task", time_limit=60)
def update_sucursal_cameras_task(sucursal):
    return xvr.update_sucursal_cameras(sucursal)

"""