# utils.py 
import time
import logging
import requests
#from   BDB_dbClass     import BDBDatabase

from   .VRecCamera      import ProcessVideoList
from   .VRecWSClient    import VRecWSClient
from   .BDB_dbClass     import BDBDatabase

from    .mysqlmodels.models import CamaraVideoLost
from    datetime        import datetime



class XVR():
    def __init__(self,bdb) -> None:
        count = 0
        #self.bdb = BDBDatabase()
        self.bdb = bdb
        #self.XVRIP = self.bdb.GetVRecIP()
    
    def update_sucursal_cameras_status(self,sucursal):
        logging.info(f"XVR.update_sucursal_cameras_status(): {numeroSuc} {sucursal}")  
        numeroSuc = sucursal[0]
        vrecHost  = sucursal[1]
        vrecPost  = sucursal[2]
        self.bdb.WriteLog(numeroSuc, "Started")

        vrec = VRecWSClient(vrecHost, port=vrecPost, sucursal=numeroSuc)

        if (vrec.exception):
            self.bdb.WriteLog(numeroSuc, vrec.exception)
            self.bdb.UpdateStatus(numeroSuc, vrec.exception)
        else:
            self.bdb.UpdateStatus(numeroSuc, "Online")
        
        if (vrec.client and not vrec.exception): # and numeroSuc == 105):
            self.bdb.WriteLog(numeroSuc, "CameraList")        
            cameras = vrec.GetCameraList()
            for cameraId in cameras:
                self.bdb.WriteLog(numeroSuc, f"CameraId:{cameraId}")
                camera = vrec.GetCameraData(cameraId)
                #videoList = vrec.GetCameraVideoList(cameraId)
                if 1:
                    #self.bdb.WriteLog(numeroSuc, f"VideoListt:{cameraId}")
                    #print("VideoList: ", videoList)
                    #firstDate, lastDate, lost = ProcessVideoList(videoList)
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
                    #camaraInfo['firstDate']      = str(firstDate)
                    #camaraInfo['lastDate']       = str(lastDate)
                    #camaraInfo['lost']           = lost
                    """
                    file = open('resumenProceso.txt','a+')  
                    file.write("\n")
                    file.write(f"sucursal:{numeroSuc}, cameras:{len(cameras)},videos_lost:{len(lost)} ")
                    file = open('logslost22.txt','a+')  
                    if lost:
                        for lost_segment in lost:
                            logging.info(f"Lost(): {camaraInfo['sucursal'] , camaraInfo['camara'] ,lost_segment } ")
                            if len(lost_segment) == 2:
                                #queryStr = f"INSERT INTO camara_video_lost VALUES({camaraInfo['sucursal']}, {camaraInfo['camara']}, '{lost_segment[0]}'," \
                                #        f"'{lost_segment[1]}','{0}', '2022-12-07 10:00:09')"
                                print(lost_segment)
                                file.write("\n")
                                file.write(f"video_lost {camaraInfo['sucursal']} {camaraInfo['camara']} - {lost_segment[0]} {lost_segment[1]} ")
                    self.bdb.UpdateCameraLost(camaraInfo, lost)"""
                    self.bdb.UpdateCameraRecord(camaraInfo)
        try:
            vrec = None
            self.bdb.WriteLog(numeroSuc, "Finished")
            return f"Terminando Sucursal: {numeroSuc}:'{vrecHost}'"
        except:
            self.bdb.WriteLog(numeroSuc, "Exception")
            return "EXCEPTION"
        #return "Terminado"

    def update_sucursal_cameras2(self,sucursal):
        logging.info(f"ProcessXVR.update_sucursal_cameras ({sucursal})")
        numeroSuc = sucursal[0]
        vrecHost  = sucursal[1]
        vrecPost  = sucursal[2]
        logging.info(f" Procesando Sucursal: {numeroSuc} {sucursal}")    
        vrec = VRecWSClient(vrecHost, port=vrecPost, sucursal=numeroSuc)
        camerasInfo = []
        if (vrec.client): # and numeroSuc == 105):
            cameras = vrec.GetCameraList()
            print("Len cameraList():",len(cameras))
            for cameraId in cameras:
                camera = vrec.GetCameraData(cameraId)
                videoList = vrec.GetCameraVideoList(cameraId)
                if not videoList:
                    print(f"videoList returned None{videoList}{cameraId}")
                    videoList = vrec.GetCameraVideoList(cameraId)
                    videoList = vrec.GetCameraVideoList(cameraId)

                #print(f"\n videos:{len(videoList)}")
                #f = open('camera_list.txt','a+')  
                #f.write(f"\n videos:{len(videoList)}")
                #f.close()
                if (videoList):
                    #print("VideoList: ", videoList)
                    firstDate, lastDate, lost = ProcessVideoList(videoList)

                    f = open('camera_list.txt','a+')  
                    f.write(f"\n sucursal: {numeroSuc} cameras:{len(cameras)} cameraId:{cameraId} videos: {len(videoList)}videoLost:{len(lost)}")
                    print(f"\n sucursal:{numeroSuc}cameras:{len(cameras)}cameraId:{cameraId}videos:{len(videoList)}videoLost:{len(lost)}")
                    f.close()

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
                    camaraInfo['lost']           = lost
                    camerasInfo.append(camaraInfo)
                    
                    """file = open('logslost22.txt','a+')  
                    if lost:
                        for lost_segment in lost:
                            logging.info(f"Lost(): {camaraInfo['sucursal'] , camaraInfo['camara'] ,lost_segment } ")
                            if len(lost_segment) == 2:
                                #queryStr = f"INSERT INTO camara_video_lost VALUES({camaraInfo['sucursal']}, {camaraInfo['camara']}, '{lost_segment[0]}'," \
                                #        f"'{lost_segment[1]}','{0}', '2022-12-07 10:00:09')"
                                print(lost_segment)
                                file.write("\n")
                                file.write(f"video_lost {camaraInfo['sucursal']} {camaraInfo['camara']} - {lost_segment[0]} {lost_segment[1]} ")"""
                    self.bdb.UpdateCameraRecord(camaraInfo)
                    self.bdb.UpdateCameraLost(camaraInfo, lost)
                    #return camerasInfo

        return "Terminado"
    
    def update_sucursal_cameras(self,sucursal):
        logging.info(f"ProcessXVR.update_sucursal_cameras ({sucursal})")
        numeroSuc = sucursal[0]
        vrecHost  = sucursal[1]
        vrecPost  = sucursal[2]
        logging.info(f" Procesando Sucursal: {numeroSuc} {sucursal}")  
        self.bdb.WriteLog(numeroSuc, "Started")

        vrec = VRecWSClient(vrecHost, port=vrecPost, sucursal=numeroSuc)

        if (vrec.exception):
            self.bdb.WriteLog(numeroSuc, vrec.exception)
            self.bdb.UpdateStatus(numeroSuc, vrec.exception)
        else:
            self.bdb.UpdateStatus(numeroSuc, "Online")
        
        if (vrec.client and not vrec.exception): # and numeroSuc == 105):
            self.bdb.WriteLog(numeroSuc, "CameraList")        
            cameras = vrec.GetCameraList()
            for cameraId in cameras:
                
                

                self.bdb.WriteLog(numeroSuc, f"CameraId:{cameraId}")

                camera = vrec.GetCameraData(cameraId)
                videoList = vrec.GetCameraVideoList(cameraId)
                if (videoList):
                    self.bdb.WriteLog(numeroSuc, f"VideoListt:{cameraId}")
                    
                    #print("VideoList: ", videoList)
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
                    camaraInfo['lost']           = lost

                    file = open('resumenProceso.txt','a+')  
                    file.write("\n")
                    file.write(f"sucursal:{numeroSuc}, cameras:{len(cameras)},videos_lost:{len(lost)} ")
                    file = open('logslost22.txt','a+')  
                    if lost:
                        for lost_segment in lost:
                            logging.info(f"Lost(): {camaraInfo['sucursal'] , camaraInfo['camara'] ,lost_segment } ")
                            if len(lost_segment) == 2:
                                #queryStr = f"INSERT INTO camara_video_lost VALUES({camaraInfo['sucursal']}, {camaraInfo['camara']}, '{lost_segment[0]}'," \
                                #        f"'{lost_segment[1]}','{0}', '2022-12-07 10:00:09')"
                                print(lost_segment)
                                file.write("\n")
                                file.write(f"video_lost {camaraInfo['sucursal']} {camaraInfo['camara']} - {lost_segment[0]} {lost_segment[1]} ")
                    self.bdb.UpdateCameraRecord(camaraInfo)
                    self.bdb.UpdateCameraLost(camaraInfo, lost)
        try:
            vrec = None
            self.bdb.WriteLog(numeroSuc, "Finished")
            return f"Terminando Sucursal: {numeroSuc}:'{vrecHost}'"
        except:
            self.bdb.WriteLog(numeroSuc, "Exception")
            return "EXCEPTION"
        #return "Terminado"

    
    

    def update_video_lost(self, sucursalCameraInfo):
        logging.info(f"ProcessXVR.update_video_lost ()")

        for cameraInfo in sucursalCameraInfo:
            
            """logging.info(f"UpdateCameraLost()")
            #print(cameraInfo)
            lost = cameraInfo['lost']
            if lost:
                for lost_segment in lost:
                    logging.info(f"Lost(): {cameraInfo['sucursal'] , cameraInfo['camara'] ,lost_segment } ")
                    if len(lost_segment) == 2:
                        #queryStr = f"INSERT INTO camara_video_lost VALUES({cameraInfo['sucursal']}, {cameraInfo['camara']}, '{lost_segment[0]}'," \
                         #       f"'{lost_segment[1]}','{0}','{datetime.now()}')"

                        CamaraVideoLost.objects.using('bdb').create(sucursal=cameraInfo['sucursal'], camara=cameraInfo['camara'], segmento_inicio=lost_segment[0], segmento_fin=lost_segment[1], tiempo_total=0, last_update=datetime.now())"""
                    
            self.bdb.UpdateCameraRecord(cameraInfo)
            self.bdb.UpdateCameraLost(cameraInfo, cameraInfo['lost'])


            #self.bdb.UpdateCameraLost(camaraInfo, lost)

    def truncate_table(self,table):
        logging.info(f"ProcessXVR.truncate_table ({table})")
        self.bdb.TruncateTable(table)
        return "Truncado"




