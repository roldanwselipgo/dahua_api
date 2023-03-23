# Create your tasks here

from celery import shared_task
import time
from core.dahuaClasses.dahua_class import Dahua


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

@shared_task(name="get_sucursal_info", time_limit=40)
def get_sucursal_info_task(host, port, user, password):
    try:
        dvr = Dahua(host, port, user, password)
        device_type = dvr.GetDeviceType()
        dvr_serial_number = dvr.GetSerialNumber()
        
        #Get info cameras
        info = []
        devs=dvr.RemoteDevices()

        #print(f"Devs: {host} {devs} ")
        
        info.append(get_camera_info(0,devs))
        info.append(get_camera_info(1,devs))
        info.append(get_camera_info(2,devs))
        info.append(get_camera_info(3,devs))
        info.append(get_camera_info(4,devs))
        info.append(get_camera_info(5,devs))
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