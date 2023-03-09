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
        

@shared_task(name="port_scanner")
def port_scanner(address, port):
    
    timeout=10
    response=1
    i="ok"
    if 1:
        print(f"port_scanner()", flush=True)
        
        try:
            nm = nmap.PortScanner()
            r = nm.scan(address, str(port), arguments='-Pn  --max-retries 10 --host-timeout 11s')
            response = nm.all_hosts()[0]
            if response:
                host = nm.all_hosts()[0]
                response = nm[f'{host}'].tcp(port)['state']

            if response == "open":
                print (address, 'is up!', response)
                file = open('status_file.csv','a+')  
                file.write(f"{address},1\n")
                file.close()
            else:
                print (address, 'is down!', response)
                file = open('status_file.csv','a+')  
                file.write(f"{address},0\n")
                file.close()
        except:
            print (i,address, 'unresolve!', response)
            file = open('status_file.csv','a+')  
            file.write(f"{address},2\n")
            file.close()



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
    

@shared_task(name="update_sucursal_cameras_status")
def update_sucursal_cameras_status(sucursal):
    start_time = time.time()
    #print(xvr.XVRIP)
    #try:
        #rs = ResultSet([update_sucursal_cameras_status_task.delay(address) for address in xvr.XVRIP])
        #rs = ResultSet([xvr.update_sucursal_cameras_status(address) for address in xvr.XVRIP])
    if 1:
        xvr.update_sucursal_cameras_status(sucursal) 
    #except:
    #    pass

    end_time = time.time()
    print("time:", end_time - start_time)
    return str(end_time - start_time)


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