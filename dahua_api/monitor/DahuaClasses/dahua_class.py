#!/usr/bin/env python3
# Implementación de API de Dahua
#
from genericpath import exists
import re
import socket
import requests
import datetime
import pprint
import pendulum
import shutil
import math
import base64
import six 
from   datetime import datetime
from   requests.auth import HTTPDigestAuth, HTTPBasicAuth
from   icmplib       import ping
from   decimal       import Decimal
from   monitor.DahuaClasses.dahua_parse   import DahuaParse



from   requests.adapters import HTTPAdapter, Retry

DAHUA_USER          = 'admin'
DAHUA_PASS          = 'Elipgo$123'
DAHUA_PORT          = 8011
DAHUA_GETDDNS       = '/cgi-bin/configManager.cgi?action=getConfig&name=DDNS'
DAHUA_GETAUTOMNT    = '/cgi-bin/configManager.cgi?action=getConfig&name=AutoMaintain'
DAHUA_GETGRALCONF   = '/cgi-bin/configManager.cgi?action=getConfig&name=General'
DAHUA_GETSERIALNO   = '/cgi-bin/magicBox.cgi?action=getSerialNo'
DAHUA_GETHARDVER    = '/cgi-bin/magicBox.cgi?action=getHardwareVersion'
DAHUA_GETDEVTYPE    =  '/cgi-bin/magicBox.cgi?action=getDeviceType'
DAHUA_GETCURTIME    = '/cgi-bin/global.cgi?action=getCurrentTime'
DAHUA_SETCURTIME    = '/cgi-bin/global.cgi?action=setCurrentTime'
DAHUA_SETCONFIG     = '/cgi-bin/configManager.cgi?action=setConfig'
DAHUA_GETLOCALES    = '/cgi-bin/configManager.cgi?action=getConfig&name=Locales'
DAHUA_SETLOCALES    = '/cgi-bin/configManager.cgi?action=setConfig'
DAHUA_GETNTPCONF    = '/cgi-bin/configManager.cgi?action=getConfig&name=NTP'
DAHUA_SETNTPCONF    = '/cgi-bin/configManager.cgi?action=setConfig'
DAHUA_REBOOT        = '/cgi-bin/magicBox.cgi?action=reboot'
DAHUA_FINDLOGS      = '/cgi-bin/log.cgi?action=startFind'
DAHUA_DOFIND        = '/cgi-bin/log.cgi?action=doFind'
DAHUA_ATTACHFILE    = '/cgi-bin/snapManager.cgi?action=attachFileProc'
DAHUA_HDINFO        = '/cgi-bin/storageDevice.cgi?action=factory.getPortInfo'
DAHUA_HDNAMES       = '/cgi-bin/storageDevice.cgi?action=factory.getCollect'
DAHUA_HDDEVINFO     = '/cgi-bin/storageDevice.cgi?action=getDeviceAllInfo'
DAHUA_HDSTORAGE     = '/cgi-bin/storageDevice.cgi?action=getCaps'
DAHUA_GETSTGROUP    = '/cgi-bin/configManager.cgi?action=getConfig&name=StorageGroup'
DAHUA_SETHOLDTIME   = '/cgi-bin/configManager.cgi?action=setConfig'
DAHUA_FINDACCSREC   = '/cgi-bin/recordFinder.cgi?action=find&name=AccessControlCardRec'
DAHUA_DISCOVERDEV   = '/cgi-bin/deviceDiscovery.cgi?action=attach'
DAHUA_FINDLOGS      = '/cgi-bin/log.cgi?action=startFind'
DAHUA_BACKUPLOG     = '/cgi-bin/Log.backup?action='
DAHUA_GETSNAPSHOT   = '/cgi-bin/snapshot.cgi'
DAHUA_ADDUSER       = '/cgi-bin/userManager.cgi?action=addUser'
DAHUA_GETUSERINFO   = '/cgi-bin/userManager.cgi?action=getUserInfo'
DAHUA_DELETEUSER    = '/cgi-bin/userManager.cgi?action=deleteUser'
DAHUA_GETINFOUGRP   = '/cgi-bin/userManager.cgi?action=getGroupInfo'
DAHUA_DLOADFILE     = '/cgi-bin/loadfile.cgi?action=startLoad'
DAHUA_DLOADPATH     = '/cgi-bin/RPC_Loadfile'
DAHUA_GETCAPREC     = '/cgi-bin/recordManager.cgi?action=getCaps'
DAHUA_RECORDCONF    = '/cgi-bin/configManager.cgi?action=getConfig&name=Record'
DAHUA_GETGPS        = '/cgi-bin/positionManager.cgi?action=getStatus'
DAHUA_MFIND_CREATE  = '/cgi-bin/mediaFileFind.cgi?action=factory.create'
DAHUA_MFIND_FIND    = '/cgi-bin/mediaFileFind.cgi?action=findFile'
DAHUA_MFIND_NEXT    = '/cgi-bin/mediaFileFind.cgi?action=findNextFile'
DAHUA_SUB_EVENT     = '/cgi-bin/eventManager.cgi?action=attach'
DAHUA_GETMENCODE    = '/cgi-bin/configManager.cgi?action=getConfig&name=Encode'
DAHUA_SETMENCODE    = '/cgi-bin/configManager.cgi?action=setConfig'
DAHUA_SETLANGUAGE    = '/cgi-bin/configManager.cgi?action=setConfig'
DAHUA_GETAUDIOCN    = '/cgi-bin/devAudioOutput.cgi?action=getCollect'
DAHUA_POSTAUDIO     = '/cgi-bin/audio.cgi?action=postAudio'
DAHUA_OPENDOOR      = '/cgi-bin/accessControl.cgi?action=openDoor'
DAHUA_PCOUNTSUM     = '/cgi-bin/videoStatServer.cgi?action=getSummary'
DAHUA_INSERTREC     = '/cgi-bin/recordUpdater.cgi?action=insert'
DAHUA_FINDREC       = '/cgi-bin/recordFinder.cgi?action=find'
DAHUA_CLOSEFINDER   = '/cgi-bin/mediaFileFind.cgi?action=close'
DAHUA_DESTROYFINDER = '/cgi-bin/mediaFileFind.cgi?action=destroy'
DAHUA_MEDIAGLOBAL   = '/cgi-bin/configManager.cgi?action=getConfig&name=MediaGlobal'


#DAHUA_TIMEOUT      = 120
#DAHUA_TIMEOUT      = 300
DAHUA_TIMEOUT      = 300
DAHUA_PORT1        = 8011
DAHUA_PORT2        = 8012
DAHUA_PORT3        = 8013
PING_COUNT         = 10
PING_TIMEOUT       = 2
PING_INTERVAL      = 0.2




class Dahua:
   def __init__(self, sitio, port=DAHUA_PORT, user=DAHUA_USER, password=DAHUA_PASS):
      #print("DahuaClass(%s)" % sitio)

      #aa = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", sitio)
      #print("Dahua: ", sitio, port, user, password)
      if isinstance(sitio, str):
         # Maneja el sitio especial Demo
         if sitio == '0':
            self.url = 'demo.c5cdmx.elipgodns.com'
         else:
            sitio = sitio.rstrip('\r\n')
            sitio = sitio.lower()
            aa = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", sitio)
            if aa:
               self.url = sitio
            elif sitio.startswith("mc"):
               self.url = '%s.c5cdmx.elipgodns.com'%(sitio)
            else:
               self.url = 'mc%s.c5cdmx.elipgodns.com'%(sitio)
      else:
         self.url = 'mc%d.c5cdmx.elipgodns.com'%(sitio)

      #print(self.url)
      self.sitio     = sitio
      self.port      = port
      self.user      = user
      self.password  = password
      self.count     = 0

      #self.DST_Enable = false


   # Hace el ping a la direccion del sitio
   def Ping(self, count=PING_COUNT, timeout=PING_TIMEOUT, interval=PING_INTERVAL):
      hostRsp         = ping(self.url, count, timeout, interval)
      self.ping       = hostRsp
      try:
         self.ip_address = socket.gethostbyname(self.url) 
      except:
         self.ip_address = ""
      return hostRsp.is_alive


   # Obtiene la configuración de DDNS del dispositivo
   def GetDDNS(self, timeout=DAHUA_TIMEOUT):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETDDNS)
      print(req)

      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)

         # Si se recibió una respuesta correcta a la petición, procesa la info
         self.StatusCode = response.status_code
         if response.status_code == 200:
            grpAll = re.findall(r'table.DDNS\[(\d+)\]\.(.*)=(.*)\r', response.text)

            ddnsLst  = []
            index = -1

            for grp in grpAll:
               if index != int(grp[0]):
                  index = int(grp[0])
                  ddnsLst.append({'Index': index})
               ddnsLst[int(grp[0])][grp[1]] = grp[2]

            for ddns in ddnsLst:
               if ddns['Address'] == 'members.dyndns.org':
                  self.ddnsIndex = ddns['Index']
                  self.Address   = ddns['Address']
                  self.Enable    = ddns['Enable']
                  self.HostName  = ddns['HostName'] if self.Enable=='true' else "DDNS_Disabled"
                  self.KeepAlive = ddns['KeepAlive']
                  self.UserName  = ddns['UserName']
                  self.Password  = ddns['Password']                  
      except Exception:
         print(Exception)


   # Obtiene la configuración de DDNS del dispositivo
   def GetConfig(self, timeout=DAHUA_TIMEOUT):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETDDNS)
      print(req)

      ddns = {}
      self.StatusCode = 0

      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
         #print(response)
         # Si se recibió una respuesta correcta a la petición, procesa la info
         self.StatusCode = response.status_code

         if response.status_code == 200:
            list = response.text.split(sep='\r\n')
            print(list)

            # Ya que el equipo soporta varios servicios de DDNS, se debe buscar las entradas dentro
            # de la reespuesta que coincidan con el servicio DynDNS (menbers.dyndns.org)
            oind = -1
            for rec in list:
               rsplit = rec.split(sep='=')
               #print(rec, rsplit)

               if rsplit[0]:
                  ind = int(rsplit[0][11])
                  #print(ind, rsplit[1])
                  if rsplit[1] == 'members.dyndns.org':
                     oind = ind

               # Arma la respuesta unicament con los valores relacionados a DynDNS
               if rsplit[0] and oind == ind:
                  index = rsplit[0][14:]
                  ddns[index] = rsplit[1]
                  #print("- ", index, ddns[index])

            print(ddns)
            self.Address   = ddns['Address']
            #self.Enable    = ddns['Enable']
            #self.HostName  = ddns['HostName'] if self.Enable=='true' else "DDNS_Disabled"
            self.KeepAlive = ddns['KeepAlive']
            self.UserName  = ddns['UserName']
            self.Password  = ddns['Password']
            self.ddnsIndex = oind 

         #print(">>>>", self.HostName, self.KeepAlive, self.UserName, self.Password, self.StatusCode)

      except Exception:
         print(Exception)
         self.Address    = ''
         self.HostName   = ''
         self.KeepAlive  = 0
         self.UserName   = ''
         self.Password   = ''
         self.Enable     = ''
         self.StatusCode = "Exception"
         self.ddnsIndex  = 0 

      return 1 if self.StatusCode == 200 else 0


   # Set DDNS
   def SetDDNS(self, index, address, hostName, userName, password, protocol='Dyndns DDNS', port=80, enable='true', keepAlive=5):
      req ='http://%s:%d%s' % (self.url, self.port, DAHUA_SETCONFIG)
      req = req + '&DDNS[%d].Address=%s'   % (index, address)
      req = req + '&DDNS[%d].HostName=%s'  % (index, hostName)
      req = req + '&DDNS[%d].UserName=%s'  % (index, userName)
      req = req + '&DDNS[%d].Password=%s'  % (index, password)
      req = req + '&DDNS[%d].Protocol=%s'  % (index, protocol)
      req = req + '&DDNS[%d].Port=%d'      % (index, port)
      req = req + '&DDNS[%d].Enable=%s'    % (index, enable)
      req = req + '&DDNS[%d].KeepAlive=%s' % (index, keepAlive)

      print(req)
      response = ''

      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
         print('RSP: ', response)
      except Exception:
         pass


   # Obtiene la configuración de Auto Mantenimiento
   def GetAutoMaintainConfig(self):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETAUTOMNT)
      #print (req)

      response = ''
      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      except Exception:
         pass

      if response.status_code == 200:
         rdict = {}
         list = response.text.split(sep='\r\n')
         try:
            for rec in list:
               srec  = rec.split(sep='=')
               if srec[0] != '':
                  rdict[srec[0]] = srec[1]

            self.AutoRebootEnable = rdict['table.AutoMaintain.AutoRebootEnable'] if 'table.AutoMaintain.AutoRebootEnable' in rdict else ""
            self.AutoRebootDay    = rdict['table.AutoMaintain.AutoRebootDay']    if 'table.AutoMaintain.AutoRebootDay'    in rdict else ""
            self.AutoRebootHour   = rdict['table.AutoMaintain.AutoRebootHour']   if 'table.AutoMaintain.AutoRebootHour'   in rdict else ""
            self.AutoRebootMinute = rdict['table.AutoMaintain.AutoRebootMinute'] if 'table.AutoMaintain.AutoRebootMinute' in rdict else ""
         except Exception:
            pass


   # Common Call
   def CommonCall(self, API, timeout=DAHUA_TIMEOUT):
      req = 'http://%s:%d%s' % (self.url, self.port, API)
      #print (">> CommonCall:", req, timeout)

      response = ''
      rdict = {}
      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password),timeout = timeout)

         rdict['status_code'] = response.status_code
         #print(">>RSP: ", response)
      except Exception:
         #print(">>Excep: ", response)
         rdict['status_code'] = 0
         pass

      if rdict['status_code'] == 200:
      #if response.status_code == 200:
         list = response.text.split(sep='\r\n')
         try:
            for rec in list:
               srec  = rec.split(sep='=')
               if srec[0] != '':
                  rdict[srec[0]] = srec[1]
            return rdict

         except Exception:
            pass
      return rdict


   # Get General Config
   def GetGeneralConfig(self):
      #print(">> GetGeneralConfig")
      response = self.CommonCall(DAHUA_GETGRALCONF)
      print(response)

      self.Name = ""
      #if response != "":
      if response['status_code'] == 200:
         self.Name = response['table.General.MachineName'] if 'table.General.MachineName' in response else ""
      else:
         print("Response:", response['status_code'])


   # Get Hardware Version
   def GetHardwareVersion(self):
      #print(">> GetHardwareVersion")
      response = self.CommonCall(DAHUA_GETHARDVER)
      print ("RSP: ", response)

      self.HardwareVer = ""
      #if response != "":
      if response['status_code'] == 200:
         self.HardwareVer = response['version'] if 'version' in response else ""
      else:
         print("Response:", response['status_code'])


   # Get Serial Number
   def GetSerialNumber(self):
      #print(">> GetSerialNumber")
      response = self.CommonCall(DAHUA_GETSERIALNO)

      self.SerialNo = ""
      #if response != "":
      if response['status_code'] == 200:
         self.SerialNo = response['sn'] if 'sn' in response else ""
      else:
         print("Response:", response['status_code'])


   # Get Serial Number
   def GetDeviceType(self):
      #print(">> GetDeviceType")
      response = self.CommonCall(DAHUA_GETDEVTYPE)

      self.DevType = ""
      #if response != "":
      if response['status_code'] == 200:
         self.DevType = response['type'] if 'type' in response else ""
      else:
         print("Response:", response['status_code'])


   # Get Device Info
   def GetDeviceInfo(self):
      self.GetGeneralConfig()
      self.GetHardwareVersion()
      self.GetSerialNumber()
      self.GetDeviceType()


   # Set Auto Reboot options
   def SetAutoMaintainConfig(self, rebootDay=-1, rebootHour=0, rebootMinute=0):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_SETCONFIG)
      #print(req, rebootDay, rebootHour, rebootMinute)

      if int(rebootDay) >= 0:
         req = req + '&AutoMaintain.AutoRebootDay=%s'    % (rebootDay)
         req = req + '&AutoMaintain.AutoRebootHour=%s'   % (rebootHour)
         #req = req + '&AutoMaintain.AutoRebootMinute=%d' % (rebootMinute)

         #print(req)
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
         if response.status_code == 200:
            return True

      return False


   # Obtiene registros de contron de acceso
   def FindAccessControlRecord(self):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_FINDACCSREC)
      req = req + '&count=500&StartTime=1628830800'
      print(req)

      list = []
      dict = {}
      pIndex = 0
      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response, response.text)
      if response.status_code == 200:
         for line in response.iter_lines():
            x = re.search(r'(\d+)..([\w.-]+)=([\w .]+)', str(line))
            if x:
               index = int(x.group(1))
               if index != pIndex:
                  pIndex = index
                  if (dict):
                     list.append(dict)
                  dict = {}
               dict[x.group(2)] = x.group(3)
         if dict:
            list.append(dict)

         for index, record in enumerate(list):
            if 'CardName' in record:
               print("%-4s %-25.25s %2.5s %s" % (index, record['CardName'], record['CurrentTemperature'],
                                           datetime.datetime.fromtimestamp(int(record['CreateTime']))))


   # Subscribe to Event Message
   def SubEvent(self, channel = 1):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_SUB_EVENT)
      req = req + '&codes=[FaceDetection]&heartbeat=5'
      print(req)

      response = requests.get(req,auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT, stream=True)
      print("RC:", response.status_code)
      parser = DahuaParse()

      if response.status_code == 200:
         for line in response.iter_lines(chunk_size = 1024 * 1, delimiter = b'--myboundary'):
            parser.Parse(line)


   # AttachFileProc
   def AttachFileProc(self, kronos, channel=1):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_ATTACHFILE)
      #req = req + '&Flags[0]=Event&Events=[AccessControl]&heartbeat=5'
      #req = req + '&Flags[0]=Event&Events=[FaceRecognition]&heartbeat=5'
      req = req + '&Flags[0]=Event&Events=[FaceDetection]&heartbeat=5'
      req = req + '&channel=%d' % (channel)
      print(req)

      UserID = ''
      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT, stream=True)
      print("RC:", response.status_code)
      #print("Raw", response.raw)
      cType = ""
      totLen = 0 
      estado = 0           # Esperando boundary
      image = bytearray(b'')

      parser = DahuaParse()
      if response.status_code == 200:
         #for line in response.iter_lines(chunk_size = 1024):
         for line in response.iter_lines(chunk_size = 1024 * 1, delimiter = b'--myboundary'):
            parser.Parse(line)
            
         for line in response.iter_content(chunk_size = 1024 * 16):  
            # Busca el Content-Type: image/jpeg
            parser.Parse(line)
            #print (line)

            #pos = str(line).find('Content-Type: image/jpeg')
            #if pos:
            #  pos2 = str(line).find("Content-Length: ", pos)
            #reCType = re.search(r"Content-Type: \w+/\w+", line.decode('utf-8', 'ignore'))
            #print(pos, pos2)

      if response.status_code == 200:
         for line in response.iter_lines(chunk_size = 1024, delimiter=b'\r\n'):
            #print("Estado ", estado, len(line), line)
#            try:
            if estado == 0 :                                      # Esperando boundary
               print(estado, line)
               if line.decode('utf-8', 'ignore').startswith("--myboundary"):
                  print(estado, line)
                  estado = 1
            elif estado == 1:                                     # Esperando Content-Type
               #print(line)
               reCType = re.search(r"Content-Type: \w+/\w+", line.decode('utf-8', 'ignore'))
               if reCType:
                  cType = reCType.group().split(" ")[1]
                  print(estado, cType, line)
                  estado = 2
            elif estado == 2:                                     # Esperando Content-Length
               #print(line)
               reCLen = re.search(r"Content-Length: \w+", line.decode('utf-8', 'ignore'))
               if reCLen:
                  cLen = reCLen.group().split(" ")[1]
                  print(estado, cType, cLen, line)
                  if cType == "image/jpeg":
                     estado = 3                                   # Cambia a estdo de preceso de imagen
                  elif cType == 'text/plain':
                     estado = 0
            elif estado == 3:                                     # Proceso de Imagen
               totLen = totLen + len(line)
               print(estado, totLen, int(cLen), len(line), line)
               if totLen >= int(cLen):
                  with open('Imagen0.jpg', 'wb') as f:
                     f.write(image)
                  f.close()
                  image = bytearray(b'')
                  estado = 0
                  totLen = 0 
               if len(line) == 12:
                  if line.decode('utf-8', 'ignore').startswith("--myboundary"):
                     print("Saltando a estado 0 Bytes", totLen)
                     estado = 0
                     totLen = 0
                     #print(image)
                     with open('Imagen.jpg', 'wb') as f:
                        f.write(image)
                     f.close()
                     image = bytearray(b'')
                  else:
                     image += line
               else:
                  #if len(line): 
                  image += line

#            except:
               #pass 
#               print("Exception:", estado, line)


         #with open('S%s_%d.jpg' % (self.sitio, channel), 'wb') as f:
         #   response.raw.decode_content = True
         #      shutil.copyfileobj(response.raw, f)

# KRONOS
#          for line in response.iter_lines():
#             if line:
#                sline = str(line)
#                if 'Events[0].' in sline:
#                  rec = sline.split(sep='=')
#                  #print (rec)
#                  if 'CardName'           in rec[0]: CardName           = rec[1].rstrip("'")
#                  if 'CreateTime'         in rec[0]: CreateTime         = rec[1].rstrip("'")
#                  if 'CurrentTemperature' in rec[0]: CurrentTemperature = rec[1].rstrip("'")
#                  if 'ErrorCode'          in rec[0]: ErrorCode          = rec[1].rstrip("'")
#                  if 'Status'             in rec[0]: Status             = rec[1].rstrip("'")
#                  if 'UserID'             in rec[0]: UserID             = rec[1].rstrip("'")
#                  if UserID:
#                     print("%s,%s,%s,%s,%s,%s" %
#                        (UserID,CardName,ErrorCode,Status,CurrentTemperature,
#                         datetime.datetime.fromtimestamp(int(CreateTime))))
#                     kronos.Punch(UserID)
#                     UserID = ""
#                     print(CreateTime)



   # Rebootea el dispositivo
   def Reboot(self):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_REBOOT)
      #print (req)

      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.use, self.password))

      except Exception:
         print ("Reboot Exception: ")

   def FindLogs(self, startTime, endTime):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_FINDLOGS)
      req = req + '&condition.StartTime=%s' % (startTime)
      req = req + '&condition.EndTime=%s'  % (endTime)

      print(req)

      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password))
         if response.status_code == 200:
            srec = response.text.split('=')
            token = int(srec[1])
            print ("Token= ", srec[1])

            req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_DOFIND)
            req = req + '&token=%d' % (token)
            req = req + '&count=100'
            print (req)

            response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password))
            print(response, response.text)

      except Exception:
         print ("Exception")

   # Regresa el estado de los puertos
   def GetPortStatus(self, port, timeout = 10):
      #print("GetPortStatus(%s,%s)" % (self.url, port))
      siteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      siteSocket.settimeout(timeout)
      result = ""

      try:
         location = (self.url, port)
         result = "1" if siteSocket.connect_ex(location) == 0 else "0"
      except:
         #print("URL Excep: ", self.url, port)
         pass

      siteSocket.close()
      return result


   ###############################################################################
   # Funciones relacionadas con Storage
   ###############################################################################

   # Regresa la Informaci�n de los HDD's configurados
   def GetHDInfo(self):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_HDINFO)
      #print(req)
      response = ""
      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      except Exception:
         pass

      if response.status_code == 200:
         rdict = {}
         list = response.text.split(sep='\r\n')

         for rec in list:
            srec  = rec.split(sep='=')
            if srec[0] != '':
               rdict[srec[0]] = srec[1]

         print(rdict)
         self.HDBad  = rdict['info.Bad']
         self.HDIDE  = rdict['info.IDE']
         self.HDMask = rdict['info.Mask']
         self.Plug   = rdict['info.Plug']
         self.Total  = rdict['info.Total']
         self.eSATA  = rdict['info.eSATA']

      return response


   def GetHDNames(self):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_HDNAMES)
      print(req)

      response = ""
      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
         print("GetHDNames()", response.text)
      except Exception:
         #print("GetHDNames() Exception")
         pass

      return response


   def GetHDDevInfo(self):
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_HDDEVINFO)
      print(req)

      response = ""
      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      except Exception:
         pass

      #print(response)
      if response.status_code == 200:
         rdict = {}
         list = response.text.split(sep='\r\n')
         for rec in list:
            srec  = rec.split(sep='=')
            if srec[0] != '':
               rdict[srec[0]] = srec[1]

         print(rdict)
         index = 0
         for index in range(4):
            print("Index", index)
            self.HDIsError =     rdict['list.info[0].Detail[%s].IsError' % (index)]
            self.HDPath =        rdict['list.info[0].Detail[%s].Path' % (index)]
            self.HDTotBytes =    rdict['list.info[0].Detail[%s].TotalBytes' % (index)]
            self.HDType      =   rdict['list.info[0].Detail[%s].Type' % (index)]
            self.HDUsedBytes =   rdict['list.info[0].Detail[%s].UsedBytes' % (index)]
            print(self.HDIsError, self.HDPath, self.HDType, self.HDTotBytes, self.HDUsedBytes)

      return response


   ###############################################################################
   # Funciones relacionadas con configuración de horarios
   ###############################################################################
   def GetCurrentTime(self, timeout=DAHUA_TIMEOUT):
      #print(">> GetCurrentTime")
      response = self.CommonCall(DAHUA_GETCURTIME, timeout)
      print ("RSP: ", response)
      return response
      #self.HardwareVer = ""
      #if response != "":
      #if response.status_code == 200:
      #   self.HardwareVer = response['version'] if 'version' in response else ""
      #else:
      #   print("Response:", response.status_code)

   def SetCurrentTime(self, timeStamp):
      #print(">> SetCurrentTime(%s)" % (timeStamp))
      parms = 'time=%s' % (timeStamp)
      response = self.CommonCall(DAHUA_SETCURTIME + '&' + parms)
      print("RSP: ", response, response.text)
      return response


   def GetLocales(self):
      #print("GetLocales()")
      response = self.CommonCall(DAHUA_GETLOCALES)
      #print(response)
      if response['status_code'] == 200:
         self.DST_Enable      = response['table.Locales.DSTEnable']       if 'table.Locales.DSTEnable'       in response else ""
         self.DST_StartDay    = response['table.Locales.DSTStart.Day']    if 'table.Locales.DSTStart.Day'    in response else ""
         self.DST_StartHour   = response['table.Locales.DSTStart.Hour']   if 'table.Locales.DSTStart.Hour'   in response else ""
         self.DST_StartMinute = response['table.Locales.DSTStart.Minute'] if 'table.Locales.DSTStart.Minute' in response else ""
         self.DST_StartMonth  = response['table.Locales.DSTStart.Month']  if 'table.Locales.DSTStart.Month'  in response else ""
         self.DST_StartWeek   = response['table.Locales.DSTStart.Week']   if 'table.Locales.DSTStart.Week'   in response else ""
         self.DST_StartYear   = response['table.Locales.DSTStart.Year']   if 'table.Locales.DSTStart.Year'   in response else ""

         self.DST_EndDay      = response['table.Locales.DSTEnd.Day']      if 'table.Locales.DSTEnd.Day'      in response else ""
         self.DST_EndHour     = response['table.Locales.DSTEnd.Hour']     if 'table.Locales.DSTEnd.Hour'     in response else ""
         self.DST_EndMinute   = response['table.Locales.DSTEnd.Minute']   if 'table.Locales.DSTEnd.Minute'   in response else ""
         self.DST_EndMonth    = response['table.Locales.DSTEnd.Month']    if 'table.Locales.DSTEnd.Month'    in response else ""
         self.DST_EndWeek     = response['table.Locales.DSTEnd.Week']     if 'table.Locales.DSTEnd.Week'     in response else ""
         self.DST_EndYear     = response['table.Locales.DSTEnd.Year']     if 'table.Locales.DSTEnd.Year'     in response else ""
      return response



   def SetLocales(self, DST_Enable, DST_Start, DST_End):
      #print(DST_Enable, DST_Start, DST_End)
      startTS = datetime.strptime(DST_Start, "%Y-%m-%d %H:%M")
      endTS   = datetime.strptime(DST_End,   "%Y-%m-%d %H:%M")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_SETLOCALES)

      req = req + '&Locales.DSTEnable=' + DST_Enable
      req = req + '&Locales.DSTStart.Day=%d'    % (startTS.day)
      req = req + '&Locales.DSTStart.Hour=%d'   % (startTS.hour)
      req = req + '&Locales.DSTStart.Minute=%d' % (startTS.minute)
      req = req + '&Locales.DSTStart.Month=%d'  % (startTS.month)
      req = req + '&Locales.DSTStart.Week=%d'   % (0)
      req = req + '&Locales.DSTStart.Year=%d'   % (startTS.year)

      req = req + '&Locales.DSTEnd.Day=%d'      % (endTS.day)
      req = req + '&Locales.DSTEnd.Hour=%d'     % (endTS.hour)
      req = req + '&Locales.DSTEnd.Minute=%d'   % (endTS.minute)
      req = req + '&Locales.DSTEnd.Month=%d'    % (endTS.month)
      req = req + '&Locales.DSTEnd.Week=%d'     % (0)
      req = req + '&Locales.DSTEnd.Year=%d'     % (endTS.year)
      #print (startTS, endTS, req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      if response.status_code == 200:
         return(response)



   def SetLocalesByWeek(self, DST_Enable, DST_Start, DST_End):
      print("SetLocalesByWeek(%s,'%s', '%s')" % (DST_Enable, DST_Start, DST_End))

      startTS = datetime.strptime(DST_Start, "%Y-%m-%d %H:%M")
      endTS   = datetime.strptime(DST_End,   "%Y-%m-%d %H:%M")

      startPe = pendulum.from_format(DST_Start, 'YYYY-MM-DD HH:mm')
      endPe   = pendulum.from_format(DST_End,   'YYYY-MM-DD HH:mm')

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_SETLOCALES)
      req = req + '&Locales.DSTEnable=' + DST_Enable
      req = req + '&Locales.DSTStart.Day=%d'    % (0) #startTS.weekday()+1)
      req = req + '&Locales.DSTStart.Hour=%d'   % (startTS.hour)
      req = req + '&Locales.DSTStart.Minute=%d' % (startTS.minute)
      req = req + '&Locales.DSTStart.Month=%d'  % (startTS.month)
      req = req + '&Locales.DSTStart.Week=%d'   % (startPe.week_of_month)
      req = req + '&Locales.DSTStart.Year=%d'   % (startTS.year)

      req = req + '&Locales.DSTEnd.Day=%d'      % (0) #endTS.weekday()+1)
      req = req + '&Locales.DSTEnd.Hour=%d'     % (endTS.hour)
      req = req + '&Locales.DSTEnd.Minute=%d'   % (endTS.minute)
      req = req + '&Locales.DSTEnd.Month=%d'    % (endTS.month)
      #req = req + '&Locales.DSTEnd.Week=%d'     % (endPe.week_of_month)
      req = req + '&Locales.DSTEnd.Week=%d'     % (-1)
      req = req + '&Locales.DSTEnd.Year=%d'     % (endTS.year)
      #print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      if response.status_code == 200:
         return(response)

   def GetNTPConfig(self):
      response = self.CommonCall(DAHUA_GETNTPCONF)
      
      #print("GetNTPConfig() RSP: ", response)
      self.NTPAddress   = response['table.NTP.Address'] 
      self.NTPEnable    = response['table.NTP.Enable']
      self.NTPPort      = response['table.NTP.Port']
      self.NTPTimeZone  = response['table.NTP.TimeZone']
      if 'table.NTP.TimeZoneDesc' in response:
         self.NTPTZDesc    = response['table.NTP.TimeZoneDesc']
      self.NTPUpdPeriod = response['table.NTP.UpdatePeriod']

      print("GetNTPConfig()", response['status_code'])
      return response


   def SetNTPTimeZone(self, zone, description):
      print("SetNTPTimeZone()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_SETNTPCONF)
      req = req + '&NTP.TimeZone=%d'     % (zone)
      req = req + '&NTP.TimeZoneDesc=%s' % (description)
      #print (req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response)
      if response.status_code == 200:
         return(response)


   def SetNTPServer(self, ntpServer, ntpPort=123, interval=60, ntpEnable='true'):
      print("SetNTPServer()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_SETNTPCONF)
      req = req + '&NTP.Enable=%s'       % (ntpEnable)
      req = req + '&NTP.Address=%s'      % (ntpServer)
      req = req + '&NTP.Port=%d'         % (ntpPort)
      req = req + '&NTP.UpdatePeriod=%d' % (interval)
      #print (req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response)
      if response.status_code == 200:
         return(response)


   def DiscoverDevices(self, timeout=DAHUA_TIMEOUT):
      #print("DiscoverDevices()")

      response = self.CommonCall(DAHUA_DISCOVERDEV, timeout)
      if response['status_code'] == 200:
         self.devices = []

         prvIndex = '0'
         dict = {}
         for token in response:
            if 'deviceInfo' in token:
               rsplit = token.split(sep='.')
               index = re.findall(r'\d+', token)[0]
               dict[token[14:]] = response[token]

               if index != prvIndex:
                  prvIndex = index
                  self.devices.append(dict)
                  dict = {}

         if index:
            self.devices.append(dict)

      #pprint.pprint(self.devices)
      return response


   def FindLogs(self, startTime, endTime, type='All'):
      print("FindLogs: ", startTime, endTime, type)

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_FINDLOGS)
      req = req + '&condition.StartTime=%s'  % (startTime)
      req = req + '&condition.EndTime=%s'    % (endTime)
      req = req + '&condition.Type=%s'       % (type)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      if response.status_code == 200:
         print(response.text)
         return (response)


   def BackupLog(self, startTime, endTime, type='All'):
      print("BackupLog: ", startTime, endTime, type)

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_BACKUPLOG)
      req = req + '%s'                       % (type)
      req = req + '&condition.StartTime=%s'  % (startTime)
      req = req + '&condition.EndTime=%s'    % (endTime)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response)
      if response.status_code == 200:
         print(response.text)
         return (response)


   def GetSnapshot(self, channel = 1):
      print("GetSnapshot ", channel)

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETSNAPSHOT)
      req = req + '&channel=%d' % (channel)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT, stream=True)
      print(response)
      if response.status_code == 200:
         #print(response.raw)
         with open('S%s_%d.jpg' % (self.sitio, channel), 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)


   def AddUser(self, userName, userPassword, userGroup, userSharable='true', userMemo='', userReserved='false'):
      #print("AddUser '%s' en Sitio '%s'" % (userName, self.sitio))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_ADDUSER)
      req = req + '&user.Name=%s'      % (userName)
      req = req + '&user.Password=%s'  % (userPassword)
      req = req + '&user.Group=%s'     % (userGroup)
      req = req + '&user.Sharable=%s'  % (userSharable)
      req = req + '&user.Memo=%s'      % (userMemo)
      req = req + '&user.Reserved=%s'  % (userReserved)
      #print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      #print(response)
      if response.status_code == 200:
         return(response)


   def GetUserInfo(self, userName):
      #print("GetUserInfo(%s)" % (userName))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETUSERINFO)
      req = req + '&name=%s' % (userName)
      print(req)

      rdict= {}
      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      if response.status_code == 200:
         list = response.text.split(sep='\r\n')
         try:
            for rec in list:
               srec  = rec.split(sep='=')
               if srec[0] != '':
                  rdict[srec[0]] = srec[1]
            return rdict
         except Exception:
            print("Exception")
            pass


   def DeleteUser(self, userName):
      print("DeleteUser '%s' en Sitio '%s'" % (userName, self.sitio))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_DELETEUSER)
      req = req + '&name=%s' % (userName)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response)
      if response.status_code == 200:
         return(response)


   def GetGroupInfo(self, groupName):
      print("GetGroupInfo(%s) del sitio '%s'" % (groupName, self.sitio))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETINFOUGRP)
      req = req + '&name=%s' % (groupName)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response)
      if response.status_code == 200:
         return(response.text)


   def GetStorageGroup(self):
      print("GetStorageGroup() del sitio '%s'" % (self.sitio))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETSTGROUP)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response)
      if response.status_code == 200:
         print(response.text)
         return(response.text)


   def GetMediaEncode(self):
      print("GetMediaEncode() del sitio '%s'" % (self.sitio))

      #req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETMENCODE)
      req = 'http://%s:%d%s' % (self.sitio, self.port, DAHUA_GETMENCODE)
      #print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      #print(response)
      rdict = {}
      if response.status_code == 200:
         list = response.text.split(sep='\r\n')
         for rec in list:
            srec  = rec.split(sep='=')
            if srec[0] != '':
               rdict[srec[0]] = srec[1]

         #print(rdict)
         #for el in rdict:
         #   if 'AudioEnable' in el:
         #      print(el, rdict[el])
         channel = 0
         type    = 0
         try:
            self.mainResolution  = rdict['table.Encode[%d].MainFormat[%d].Video.resolution'   % (channel, type)]
            self.mainBitRate     = rdict['table.Encode[%d].MainFormat[%d].Video.BitRate'      % (channel, type)]
            self.mainCompression = rdict['table.Encode[%d].MainFormat[%d].Video.Compression'  % (channel, type)]
            self.mainFPS         = rdict['table.Encode[%d].MainFormat[%d].Video.FPS'          % (channel, type)]
            self.mainGOP         = rdict['table.Encode[%d].MainFormat[%d].Video.GOP'          % (channel, type)]

            self.secResolution   = rdict['table.Encode[%d].ExtraFormat[%d].Video.resolution'  % (channel, type)]
            self.secBitRate      = rdict['table.Encode[%d].ExtraFormat[%d].Video.BitRate'     % (channel, type)]
            self.secCompression  = rdict['table.Encode[%d].ExtraFormat[%d].Video.Compression' % (channel, type)]
            self.secFPS          = rdict['table.Encode[%d].ExtraFormat[%d].Video.FPS'         % (channel, type)]
            self.secGOP          = rdict['table.Encode[%d].ExtraFormat[%d].Video.GOP'         % (channel, type)]
         except:
            pass

      return(rdict)
      #return(response)

   # Set Media encode
   def SetMediaEncode(self, channel, typeEncode, Compression, CustomResolutionName, FPS, BitRateControl, Quality, BitRate, stream ):
      print("SetMediaEncode() del sitio '%s'" % (self.sitio))
      req ='http://%s:%d%s' % (self.sitio, self.port, DAHUA_SETMENCODE)
      req = req + '&Encode[%d].%s[%d].Video.Compression=%s'  % (channel, stream, typeEncode ,Compression)
      req = req + '&Encode[%d].%s[%d].Video.CustomResolutionName=%s'  % (channel, stream, typeEncode ,CustomResolutionName)
      req = req + '&Encode[%d].%s[%d].Video.FPS=%s'  % (channel, stream, typeEncode ,FPS)
      req = req + '&Encode[%d].%s[%d].Video.BitRateControl=%s'   % (channel, stream, typeEncode ,BitRateControl)
      req = req + '&Encode[%d].%s[%d].Video.Quality=%s'   % (channel, stream, typeEncode ,Quality)
      req = req + '&Encode[%d].%s[%d].Video.BitRate=%s'   % (channel, stream, typeEncode ,BitRate)
      
      #req = req + '&Encode[%d].MainFormat[%d].Video.UserName=%s'  % (channel, typeEncode ,userName)
      #req = req + '&Encode[%d].MainFormat[%d].Video.Password=%s'  % (channel, typeEncode ,password)
      #req = req + '&Encode[%d].MainFormat[%d].Video.Protocol=%s'  % (channel, typeEncode ,protocol)
      #req = req + '&Encode[%d].MainFormat[%d].Video.Port=%d'      % (channel, typeEncode ,port)
      #req = req + '&Encode[%d].MainFormat[%d].Video.Enable=%s'    % (channel, typeEncode ,enable)
      #req = req + '&Encode[%d].MainFormat[%d].Video.KeepAlive=%s' % (channel, typeEncode ,keepAlive)
      print(req)
      url = req.split('?')
      try:
         response = requests.get(url=url[0],params =url[1],auth=HTTPDigestAuth(self.user, self.password), timeout=3)
         if response.status_code == 200:
            return(response.status_code)
         else:
            return 0
      except :
         print("Exception")
         return 0
      print(response,response.text)
      

   
   # Set Media encode
   def SetLanguage(self, Language):
      print("SetLanguage() del sitio '%s'" % (self.sitio))
      req ='http://%s:%d%s' % (self.sitio, self.port, DAHUA_SETLANGUAGE)
      req = req + '&Language=%s'  % (Language)
      
      print(req)
      url = req.split('?')
      response = requests.get(url=url[0],params =url[1],auth=HTTPDigestAuth(self.user, self.password))
      print(response,response.text)
      if response.status_code == 200:
         return(response.text)
      else:
         return 0

   def SetCurrentTime2(self, timeStamp):
      print("SetCurrentTime2() del sitio '%s'" % (self.sitio))
      req ='http://%s:%d%s' % (self.sitio, self.port, DAHUA_SETCURTIME)
      req = req + '&time=%s'  % (timeStamp)

      print(req)
      url = req.split('?')
      response = requests.get(url=url[0],params =url[1],auth=HTTPDigestAuth(self.user, self.password))
      print(response,response.text)
      if response.status_code == 200:
         return(response.text)
      else:
         return 0




   def SetFileHoldTime(self, index = 0, holdTime = 30):
      print("SetFileHoldTime(%s, %s) del sitio '%s'" % (index, holdTime, self.sitio))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_SETHOLDTIME)
      req = req + '&StorageGroup[%s].FileHoldTime=%s' % (index, holdTime)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response)
      if response.status_code == 200:
         return(response.text)


   def GetRecordingCaps(self):
      print("GetRecordingCaps(%s)" % (self.sitio))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETCAPREC)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response.status_code)
      if response.status_code == 200:
         print(response.text)


   def RecordConfig(self):
      print("RecordingConfig(%s)" % (self.sitio))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_RECORDCONF)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      #print(response.status_code)
      #print(response.text)
      if response.status_code == 200:
         list = response.text.split(sep='\r\n')
         for line in list:
            if "Record[0]" in line:
               print(line)


   def GetMediaGlobal(self):
      print(f"GetMediaGlobal()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_MEDIAGLOBAL)
      print(req)

      response = requests.get(req,auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response.status_code)
      if response.status_code == 200:
         print(response.text)


   def GetGPSStatus(self):
      print("GetGPSStatus(%s)" % (self.sitio))
      #print(self.user, self.password)
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_GETGPS)
      print(req)

      rdict = {}
      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)

      if (response.status_code == 200):
         list = response.text.split(sep='\r\n')
         try:
            for rec in list:
               srec  = rec.split(sep='=')
               if srec[0] != '':
                  rdict[srec[0]] = srec[1]
         except Exception:
            print("Exception")
            pass

         self.latitude  = self.GeoLat(rdict["status.Latitude"])
         self.longitude = self.GeoLon(rdict["status.Longitude"])
         return rdict


   #
   # Transforma coordenadas "Dahua" en grados, minutos, segundos a localización decimal
   #
   def GeoLat(self, location, decimals = 5):
      locs = re.split(r'[ ,\[\]]+', location)
      locf = float(locs[1]) + float(locs[2])/60 + float(locs[3])/3600

      factor = 10.0 ** decimals
      return math.trunc((locf - 90.0) * factor) / factor

   def GeoLon(self, location, decimals = 5):
      locs = re.split(r'[ ,\[\]]+', location)
      locf = float(locs[1]) + float(locs[2])/60 + float(locs[3])/3600

      factor = 10.0 ** decimals
      return math.trunc((180.0 - locf) * factor) / factor


   def DownloadPath(self, filePath, fileExt='jpg', fileSize=0):
      print(f"DownloadPath('{filePath})")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_DLOADPATH)
      req = req + '/%s' % (filePath)

      print(req)
      
      #headers  = {'Content-type': 'Application/octet-stream', 'Content-Length': f'{fileSize}'}
      headers  = {'Content-type': 'application/http', 'Content-Length': f'{fileSize}'}
      
      cookies  = {}
      try:
         #print(req)
         #print(headers)

         # response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT,
         #            stream=True, headers=headers)  #, cookies=cookies)
         # #response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT, stream=True)
         # print(response.status_code)



         session = requests.session()
         
         retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[ 500, 502, 503, 504 ])
         
         session.mount('http://', HTTPAdapter(max_retries=retries))

         session.auth = HTTPDigestAuth(self.user, self.password)
         
         
         
         # session.headers.update(
         #    {'Content-type': 'Application/octet-stream', 'Content-Length': f'{fileSize}'}
         # )
         response = session.get(req)
         print(">> response:", response.status_code)
         print(">> response:", response.text)
         if response.ok:
            response = session.get(gh_url)
            if response.ok:
               print(response.cookies)
         exit()
         
         
         s = requests.Session()
         # retries = Retry(total=5,
         #        backoff_factor=0.1,
         #        status_forcelist=[ 500, 502, 503, 504 ])
         
         # s.mount('http://', HTTPAdapter(max_retries=retries))
         # s.headers.update(
         #    {'Content-type': 'Application/octet-stream', 'Content-Length': f'{fileSize}'}
         # )

         response = s.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT
                      )

         print(response, len(response.content))
         if response.status_code == 200:
            print(response.text)

         if response.status_code == 200:
            #print(response.raw)
            local_filename = req.split('/')[-1]            
            with open(local_filename, 'wb') as f:
               response.raw.decode_content = True
               shutil.copyfileobj(response.raw, f)

      except requests.exceptions.RequestException as e:  # This is the correct syntax
         raise SystemExit(e)         
      return 


      if response.status_code == 200:
         #print(response.headers)
         print(response, len(response.content))
         #print(response.content)

         with open('S%s_%d.%s' % (self.sitio, self.count, fileExt), 'wb') as f:
            #response.content.decode_content = True
            #shutil.copyfileobj(str(response.content), f)
            f.write(response.content)
            self.count = self.count + 1


   def DownloadFile(self, channel, startTime, endTime, typeNo = 0):
      #print("DownloadFile(%s, %s, '%s', '%s', %s)" % (self.sitio, channel, startTime, endTime, typeNo))

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_DLOADFILE)
      req = req + '&channel=%s'   % (channel)
      req = req + '&subtype=%s'   % (typeNo)
      req = req + '&startTime=%s' % (startTime)
      req = req + '&endTime=%s'   % (endTime)
      print(req)

      #headers  = {'Content-type': 'Application/octet-stream'}
      headers  = {'Content-type': 'application/http'}
      
      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT, 
                 stream=True, headers=headers)

      #print(response.headers)
      print(response, len(response.content))

      if response.status_code == 200:
         print("Content-type:  ", response.headers['Content-type'])
         print("Content_Length:", response.headers['CONTENT-LENGTH'])
         print(response.text)



   def MediaFindFileCreate(self):
      #print("MediaFindFileCreate()")

      self.MFINDObject = ''
      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_MFIND_CREATE)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      #print(response, len(response.content))
      if response.status_code == 200:
         rdict = {}
         list = response.text.split(sep='\r\n')
         for rec in list:
            srec  = rec.split(sep='=')
            if srec[0] != '':
               rdict[srec[0]] = srec[1]
               self.MFINDObject  = rdict['result']

               #print("RESULT:", self.MFINDObject)
      else:
         print(f"ResponseCode: {response.status_code}")


   def MediaFindFile(self, channel, startTime, endTime):
      print("MediaFindFile()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_MFIND_FIND)
      req = req + '&object=%s'              % (self.MFINDObject)
      req = req + '&condition.Channel=%s'   % (channel)      
      req = req + '&condition.StartTime=%s' % (startTime)
      req = req + '&condition.EndTime=%s'   % (endTime)
      #req = req + '&condition.Types[0]=dav'
      #req = req + '&condition.Flags[0]=Timing'
      req = req + '&condition.VideoStream[0]=Main'      
      #req = req + '&condition.VideoStream[0]=Extra1fdsasadgfds'
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response, len(response.content))
      if response.status_code == 200:
         print(response.text)


   def MediaFindFileFR(self, channel, startTime, endTime):
      #print("MediaFindFileFR()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_MFIND_FIND)
      req = req + '&object=%s'            % (self.MFINDObject)
      req = req + '&condition.Channel=%s' % (channel)
      req = req + '&condition.Types[0]=jpg'
      req = req + '&condition.Flags[0]=Event'
      req = req + '&condition.Events[0]=FaceRecognition'
      req = req + '&condition.DB.FaceRecognitionRecordFilter.RegType=RecSuccess'
      req = req + '&condition.DB.FaceRecognitionRecordFilter.StartTime=%s' % (startTime)
      req = req + '&condition.DB.FaceRecognitionRecordFilter.EndTime=%s'    % (endTime)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print("MediaFindFile",response, len(response.content))
      if response.status_code == 200:
         print(response.text)

      # s = requests.Session()
      # '''s.headers.update({'Authorization': 'Bearer {token}'})'''
      # response = s.get('https://reqbin.com/echo/get/json', auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      # print(response, len(response.content))
      # if response.status_code == 200:
      #    print(response.text)

   



   def MediaFindFileFD(self, channel, startTime, endTime):
      #print("MediaFindFileFD()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_MFIND_FIND)
      req = req + '&object=%s'            % (self.MFINDObject)
      req = req + '&condition.Channel=%s' % (channel)
      req = req + '&condition.StartTime=%s' % (startTime)
      req = req + '&condition.EndTime=%s'    % (endTime)
      req = req + '&condition.Types[0]=jpg'
      req = req + '&condition.Flags[0]=Event'
      req = req + '&condition.Events[0]=FaceDetection'
      #req = req + '&condition.DB.FaceRecognitionRecordFilter.RegType=RecSuccess'      
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response, len(response.content))
      if response.status_code == 200:
         print(response.text)


   def MediaFindFileLPR(self, channel, startTime, endTime):
      print(f"MediaFindFileLPR({channel},{startTime}, {endTime})")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_MFIND_FIND)
      req = req + '&object=%s'            % (self.MFINDObject)
      req = req + '&condition.Channel=%s' % (channel)
      req = req + '&condition.StartTime=%s' % (startTime)
      req = req + '&condition.EndTime=%s'    % (endTime)
      req = req + '&condition.Types[0]=jpg'
      req = req + '&condition.Flags[0]=Event'
      req = req + '&condition.Events[0]=PlateNumber'
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response, len(response.content))
      if response.status_code == 200:
         print(response.text)


   def MediaFindNextFile(self, count=100):
      print("MediaFindNextFile()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_MFIND_NEXT)
      req = req + '&object=%s'   % (self.MFINDObject)
      req = req + '&count=%s'    % (count)
      req = req + '&GroupID'
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response, len(response.content))
      if response.status_code == 200:
         print(response.text)
         return response


   # Cierra el Finder previamente generado
   def MediaCloseFinder(self):
      print("MediaCloseFinder()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_CLOSEFINDER)
      req = req + '&object=%s'   % (self.MFINDObject)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response, len(response.content))
      if response.status_code == 200:
         #print(response.text)
         return response



   # Destruye el Finder previamente generado
   def MediaDestroyFinder(self):
      print("MediaDestroyFinder()")      

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_DESTROYFINDER)
      req = req + '&object=%s'   % (self.MFINDObject)
      print(req)

      response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
      print(response, len(response.content))
      if response.status_code == 200:
         #print(response.text)
         return response


   # Get General Config
   def GetAudioOutputChannels(self):
      print(">> GetAudioOutputChannels()")
      response = self.CommonCall(DAHUA_GETAUDIOCN)
      print(response)


   # Post Audio
   def PostAudio(self, data):
      print(">> PostAudio()")

      post = 'http://%s:%d%s' % (self.url, self.port, DAHUA_POSTAUDIO)
      post = post + '&httptype=singlepart'
      post = post + '&channel=1'

      dataLen = len(data)
      headers  = { 
                    'Content-type':   'Audio/G.711A', 
                    'Content-Length': '9999999'
                 }
      print(post)
      print(headers)
      
      try:
         response = requests.post(post, auth=HTTPDigestAuth(self.user, self.password), headers=headers, data=data, timeout=5)
         print(response)         
      except requests.exceptions.RequestException as e:
         print("Exception: ", e)


   # Post Audio File 
   def PostAudioFile(self, fileName, channel=1, audioFormat='G.711A'):
      #print(">> PostAudioFile()")

      files = {'file': open(fileName, 'rb')}

      post = 'http://%s:%d%s' % (self.url, self.port, DAHUA_POSTAUDIO)
      post = post + '&httptype=singlepart'
      post = post + '&channel={0}'.format(channel)
      
      headers  = { 
                    'Content-type':   'audio/{0}'.format(audioFormat), 
                    'Content-Length': '9999999'
                 }
      print(post)
      print(headers)
      
      try:
         response = requests.post(post, auth=HTTPDigestAuth(self.user, self.password), files=files, timeout=15, headers=headers)
         print(response)         
      except requests.exceptions.RequestException as e:
         print("Exception: ", e)


   # Open Door (Access Control Device)
   def OpenDoor(self, channel=1, userId=6, type='Remote'):
      print(f"OpenDoor({channel},{userId}, {type})")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_OPENDOOR)
      req = req + f"&channel={channel}"
      req = req + f"&UserID={userId}"
      req = req + f"&type={type}"
      print(req)

      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
         print(response)
         if response.status_code == 200:
            return(response.text)
      except:
         print("Exception")


   # People Count Analytics Summary   
   def GetPCountingSummary(self, channel=1):
      print(f"GetPCountingSummary({channel})")

      response = self.CommonCall(DAHUA_PCOUNTSUM)
      print(response)


   def InsertLPRWRecord(self, plateNumber, owner, beginTime, cancelTime, openGate="true"):
      print(f"InsertLPRWRecord({plateNumber},{owner})")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_INSERTREC)
      req = req + f"&name=TrafficRedList"
      req = req + f"&PlateNumber={plateNumber}"
      req = req + f"&BeginTime={beginTime}"
      req = req + f"&CancelTime={cancelTime}"
      req = req + f"&MasterOfCar={owner}"
      req = req + f"&AuthorityList.OpenGate={openGate}"
      print(req)

      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
         print(response)
         if response.status_code == 200:
            return(response.text)
      except:
         print("Exception")


   def GetLPRRecord(self):
      print(f"GetLPRRecord()")

      req = 'http://%s:%d%s' % (self.url, self.port, DAHUA_FINDREC)
      req = req + f"&name=TrafficRedList"
      #req = req + f"&PlateNumber={plateNumber}"
      #req = req + f"&BeginTime={beginTime}"
      #req = req + f"&CancelTime={cancelTime}"
      #req = req + f"&MasterOfCar={owner}"
      print(req)

      try:
         response = requests.get(req, auth=HTTPDigestAuth(self.user, self.password), timeout=DAHUA_TIMEOUT)
         print(response)
         if response.status_code == 200:
            return(response.text)
      except:
         print("Exception")      
