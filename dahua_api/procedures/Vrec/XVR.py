# utils.py 
import time
import logging
import requests
#from   BDB_dbClass     import BDBDatabase

from   .VRecCamera      import ProcessVideoList
from   .VRecWSClient    import VRecWSClient
from   .BDB_dbClass     import BDBDatabase




class XVR():
    def __init__(self) -> None:
        count = 0
        self.bdb = BDBDatabase()
        self.XVRIP = self.bdb.GetVRecIP()
    
    def update_sucursal_cameras_status(self,sucursal):
        #logging.info(f"ProcessXVR.update_sucursal_cameras ({sucursal})")
        numeroSuc = sucursal[0]
        vrecHost  = sucursal[1]
        vrecPost  = sucursal[2]
        logging.info(f"Procesando Sucursal: {numeroSuc} {sucursal}")    
        vrec = VRecWSClient(vrecHost, port=vrecPost, sucursal=numeroSuc)
        if (vrec.client): # and numeroSuc == 105):
            cameras = vrec.GetCameraList()
            for cameraId in cameras:
                camera = vrec.GetCameraData(cameraId)
                if camera:
                    camaraInfo = {}
                    camaraInfo['sucursal']       = numeroSuc
                    camaraInfo['camara']         = camera["CameraID"]
                    camaraInfo['status']         = camera["Status"]
                    camaraInfo['enable']         = camera["Enable"]
                    self.bdb.UpdateCameraStatus(camaraInfo)

        return "Terminado"

    def update_sucursal_cameras(self,sucursal):
        logging.info(f"ProcessXVR.update_sucursal_cameras ({sucursal})")
        numeroSuc = sucursal[0]
        vrecHost  = sucursal[1]
        vrecPost  = sucursal[2]
        logging.info(f" Procesando Sucursal: {numeroSuc} {sucursal}")    
        vrec = VRecWSClient(vrecHost, port=vrecPost, sucursal=numeroSuc)
        camerasInfo = []
        if (vrec.client): # and numeroSuc == 105):
            cameras = vrec.GetCameraList()
            for cameraId in cameras:
                camera = vrec.GetCameraData(cameraId)
                videoList = vrec.GetCameraVideoList(cameraId)
                if (videoList):
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
                    camerasInfo.append(camaraInfo)

                    #self.bdb.UpdateCameraRecord(camaraInfo)
                    #self.bdb.UpdateCameraLost(camaraInfo, lost)
        return camerasInfo
    

    def update_video_lost(self, sucursalCameraInfo):
        logging.info(f"ProcessXVR.update_video_lost ()")

        for cameraInfo in sucursalCameraInfo:
            self.bdb.UpdateCameraRecord(cameraInfo)
            self.bdb.UpdateCameraLost(cameraInfo, cameraInfo['lost'])
            #self.bdb.UpdateCameraLost(camaraInfo, lost)

    def truncate_table(self,table):
        logging.info(f"ProcessXVR.truncate_table ({table})")
        self.bdb.TruncateTable(table)
        return "Truncado"




