# Create your tasks here

from celery import shared_task
import time
from core.dahuaClasses.dahua_class import Dahua
from procedures.Vrec.BDB_dbClass import BDBDatabase
from datetime import datetime, timedelta


bdb   = BDBDatabase()

def get_camera_info(camera_id,devs):
    tmp = []
    tmp.append(f'c{camera_id+1}')
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.Address']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.Address' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.Name']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.Name' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.DeviceType']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.DeviceType' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.HttpPort']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.HttpPort' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.HttpsPort']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.HttpsPort' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.Port']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.Port' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.Version']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.Version' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.AudioInputChannels']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.AudioInputChannels' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.VideoInputChannels']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.VideoInputChannels' in devs else tmp.append(None)
    tmp.append(devs[f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.VideoInputs[0].Name']) if f'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_{camera_id}.VideoInputs[0].Name' in devs else tmp.append(None)
    return tmp 

def get_video_segment(channel,starttime,endtime):
    tmp = []

@shared_task(name="get_sucursal_info", time_limit=90)
def get_sucursal_info_task(host, port, user, password, suc):
    try:
        
        dvr = Dahua(host, port, user, password)
        #dvr = Dahua("10.200.3.20", 80, "admin", "Elipgo$123")
        device_type = dvr.GetDeviceType()
        #dvr_serial_number = dvr.GetSerialNumber()
        dvr_serial_number = dvr.GetSerialNumber()
        print(">>>RecordStatusss")
        print(">>>RecordStatusss")

        by_channels = []
        #file = open('result_segmentos.csv','w+')
        #file.write("")
        #file.close()
        """
        #Otro proces---------
        bdb.open_connection()  
        file = open('result_segmentos.csv','a+')

        dvr.MediaFindFileCreate() 

        #Ejecutar el proceso a la fecha de ayer
        today = datetime.now() 
        #today = datetime.strptime("2023-04-13", "%Y-%m-%d") 
        yesterday = today - timedelta(days=1)
        today.strftime('%Y-%m-%d')
        yesterday.strftime('%Y-%m-%d')
        today = str(today.date())
        yesterday = str(yesterday.date())
        #for channel in range(1,8):
        if 1:
            rsp = dvr.MediaFindFile(-1, f"{yesterday}%2018:00:00", f"{today}%2012:00:00")
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
                            #Insertar a base
                            
                            
                            bdb.lock.acquire()
                            mycursor = bdb.connection.cursor()
                            query1=f"SELECT * from segmento_video where sucursal={suc} and ip='{host}' and channel={int(channel)} and starttime='{starttime}' and endtime='{endtime}'"
                            #print(queryStr)
                            result=None
                            try:
                                mycursor.execute(query1)
                                result = mycursor.fetchall()
                            except:
                                pass

                            if result:
                                mycursor.execute(f"INSERT INTO segmento_video (sucursal,ip,channel, starttime,endtime) VALUES ({suc}, '{host}',{int(channel)},'{starttime}','{endtime}');")
                                bdb.connection.commit()
                            mycursor.close()
                            bdb.lock.release()
                        '''
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
                        bdb.close_connection()'''

                else:
                    var = 0
            by_channels.append(segmentos)
            #print(segmentos)
        #print(by_channels)
        file.close()
        bdb.close_connection() 
        return None
        """
        
        


        #rsp = dvr.MediaFindFileFR(2, "2023-01-01%2008:00:00", "2023-01-04%2012:00:00")
        #response = dvr.MediaFindNextFile(10)
        
        #Get info cameras
        info = []
        devs=dvr.RemoteDevices()

        #print(f"Devs: {host} {devs} ")
        for i in range(0,29):
            info.append(get_camera_info(i,devs))
            #info.append(get_camera_info(i,devs))
            #info.append(get_camera_info(i,devs))
            #info.append(get_camera_info(i,devs))
            #info.append(get_camera_info(i,devs))
            #info.append(get_camera_info(i,devs))
        
        print(info)
        
        #print(devs)
        return device_type,dvr_serial_number,info
    except:
        return None
    '''
        dvr_serial_number = dvr.GetSerialNumber()
        d = dvr.DiscoverDevices()
        devs=dvr.RemoteDevices()
        ip0 = devs['table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_0.Address'] if 'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_0.Address' in devs else "0"
        ip1 = devs['table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_1.Address'] if 'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_1.Address' in devs else "0"
        ip2 = devs['table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_2.Address'] if 'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_2.Address' in devs else "0"
        ip3 = devs['table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_3.Address'] if 'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_3.Address' in devs else "0"
        ip4 = devs['table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_4.Address'] if 'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_4.Address' in devs else "0"
        ip5 = devs['table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_5.Address'] if 'table.RemoteDevice.uuid:System_CONFIG_NETCAMERA_INFO_5.Address' in devs else "0"
        ips = []
        ips.append(ip0)
        ips.append(ip1)
        ips.append(ip2)
        ips.append(ip3)
        ips.append(ip4)
        ips.append(ip5)
        """print(">>>>>>>>>>>>:IPs",ips)
        print(ips[0],ip0,"ip0")
        print(ips[1],ip1,"ip1")
        print(ips[2],ip2)
        print(ips[3],ip3)
        print(ips[4],ip4)
        print(ips[5],ip5)

        e = d[1]
        d = d[0]
        cameras_by_api=[]
        #print(f"e: {e} ")
        file = open('ips.csv','a+')  
        if d:
            for device in d:
                print(f"host:device,{host} , {device['IPv4Address.IPAddress']}")
                
                file.write(f"host:device,{host} , {device['IPv4Address.IPAddress']}")
                file.write(f"\n")
                cameras_by_api.append(device['IPv4Address.IPAddress'])
        """

        camera_data = []
        #for i,camera in enumerate(cameras):
        #for i,camera in enumerate(cameras_by_api):
        for i,camera in enumerate(ips):
            cam = Dahua(camera, port, user, password)
            camera_model = cam.GetDeviceType()
            serial_number = cam.GetSerialNumber()
            camera_data.append([f"c{i+1}",camera,camera_model,serial_number])
            #print(f"cam: {camera_data}")
        return device_type,dvr_serial_number,camera_data
    except:
        return 0


    '''