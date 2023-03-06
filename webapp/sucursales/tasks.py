# Create your tasks here

from celery import shared_task
import time
from core.dahuaClasses.dahua_class import Dahua


@shared_task(name="get_sucursal_info", time_limit=60)
def get_sucursal_info_task(host, port, user, password):
    try:
        dvr = Dahua(host, port, user, password)
        general = dvr.GetGeneralConfig()
        device_type = dvr.GetDeviceType()
        print(general)
        return device_type
    except:
        return 0