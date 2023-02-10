# Create your tasks here

from celery import shared_task
import time
from celery.result import allow_join_result
from .models import Procedure
from procedures.Vrec.XVR import XVR 
import logging
#from procedures.views import update_lost 

"""@shared_task(name="GetMediaEncodeA", time_limit=60)
def GetMediaEncodeA(host, port, user, password, id_sitio):
    try:
        dvr = Dahua(host, port, user, password)
        #video_encode_settings = dvr.GetMediaEncode() 
        config = Conf({},{},dvr)
        #---------- Obtener Configuracion de video -------------
        configs =  config.GetMediaEncodeConfig(0,0)
    except:
        return 0
    return configs

@shared_task(name="GetAllMediaEncode", time_limit=12)
def GetAllMediaEncode(host, port, user, password):
    dvr = Dahua(host, port, user, password)
    video_encode_settings = dvr.GetMediaEncode() 
    return video_encode_settings

"""








@shared_task(name="task_video_lost")
def task_video_lost():
    xvr = XVR()
    task_queue = []
    xvr.truncate_table('camara_video_lost')
    for sucursal in xvr.XVRIP[:5]:
        print("Sucursal: ",sucursal)
        task = update_sucursal_cameras.delay(sucursal)
        print("Task added: ", task)
        task_queue.append((task,sucursal))
    
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
                if 1:
                    with allow_join_result():
                        result = task[0].get()
                    #print("Resultado de tarea: ", result)
                    task_queue.remove(task)
                    print("\nlen task_queue:", len(task_queue))
                #except Exception as e: 
                #    print(f"Err en {task}: ", e)
                #    task_queue.remove(task)
                #    print("len task_queue:", len(task_queue))
                #    break
                #finally:
                    xvr.update_video_lost(result)
                    break

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


@shared_task(name="update_sucursal_cameras")
def update_sucursal_cameras(sucursal):
    xvr = XVR()
    start_time = time.time()
    if 1:
        cameraInfo = xvr.update_sucursal_cameras(sucursal) 
    end_time = time.time()
    print("time:", end_time - start_time)
    return cameraInfo
"""    
@shared_task(name="celery.get_sucursales")
@app.route('/sucursales')
def update_sucursal_cameras():
    start_time = time.time()
    try:
        xvr.truncate_table('camara_video_lost')
        rs = ResultSet([update_sucursal_cameras_task.delay(address) for address in xvr.XVRIP])
        rs.get()
    except:
        pass
    end_time = time.time()
    print("CelerySquirrel:", end_time - start_time)
    return str(end_time - start_time)
"""

@shared_task(name="status_sucursal", time_limit=32)
def sucursal():
    xvr.update_sucursal_cameras_status(101)
    return 'Sucursal procesada'


"""

@shared_task(name="celery.update_sucursal_cameras_status_task", time_limit=32)
def update_sucursal_cameras_status_task(sucursal):
    return xvr.update_sucursal_cameras_status(sucursal)

@shared_task(name="celery.update_sucursal_cameras_task", time_limit=60)
def update_sucursal_cameras_task(sucursal):
    return xvr.update_sucursal_cameras(sucursal)

"""