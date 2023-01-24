#from dahua_class import Dahua
from monitor.dahuaClasses.dahua_class import Dahua

from datetime import datetime

#dvr = Dahua("10.200.3.101", 80, "admin", "Elipgo$123")
class Config():
    def __init__(self, default_media_config = {}, default_general_config = {} , dvr = None ):
        self.dvr = dvr
        self.current_media_config_mainstream = {}
        self.current_media_config_substream = {}
        self.default_media_config = default_media_config
        self.default_general_config = default_general_config

    def ChannelCount(self):
        rdict = self.dvr.GetMediaEncode() 
        channels = 0
        for el in rdict:
            if 'Encode[%d]' % (channels) in el:
                channels = channels + 1
        print("Channels: ",channels)
        return channels
            



    def GetMediaEncodeConfig(self, channel = 0, type = 0):
        rdict = self.dvr.GetMediaEncode()
        #Inicializar Mainstream
        self.current_media_config_mainstream["Compression"] = None
        self.current_media_config_mainstream["CustomResolutionName"] = None
        self.current_media_config_mainstream["FPS"] = None
        self.current_media_config_mainstream["Quality"] = None
        self.current_media_config_mainstream["BitRateControl"] = None
        self.current_media_config_mainstream["BitRate"] = None
        #Inicializar Substream
        self.current_media_config_substream["Compression"] = None
        self.current_media_config_substream["CustomResolutionName"] = None
        self.current_media_config_substream["FPS"] = None
        self.current_media_config_substream["Quality"] = None
        self.current_media_config_substream["BitRateControl"] = None
        self.current_media_config_substream["BitRate"] = None
        self.current_media_config_substream["VideoEnable"] = None
        for el in rdict:
            #print(el)
            if 'Encode[%d].MainFormat[%d]' % (channel, type) in el:
                if 'Encode[%d].MainFormat[%d].Video.Compression' % (channel, type) in el:
                    self.current_media_config_mainstream["Compression"] = rdict['table.Encode[%d].MainFormat[%d].Video.Compression'  % (channel, type)] 
                if 'Encode[%d].MainFormat[%d].Video.CustomResolutionName' % (channel, type) in el:
                    self.current_media_config_mainstream["CustomResolutionName"] = rdict['table.Encode[%d].MainFormat[%d].Video.CustomResolutionName'   % (channel, type)]
                if 'Encode[%d].MainFormat[%d].Video.FPS' % (channel, type) in el:
                    self.current_media_config_mainstream["FPS"] = rdict['table.Encode[%d].MainFormat[%d].Video.FPS'          % (channel, type)]
                if 'Encode[%d].MainFormat[%d].Video.Quality' % (channel, type) in el:
                    self.current_media_config_mainstream["Quality"] = rdict['table.Encode[%d].MainFormat[%d].Video.Quality'      % (channel, type)]
                if 'Encode[%d].MainFormat[%d].Video.BitRateControl' % (channel, type) in el:
                    self.current_media_config_mainstream["BitRateControl"] = rdict['table.Encode[%d].MainFormat[%d].Video.BitRateControl'      % (channel, type)]
                if 'Encode[%d].MainFormat[%d].Video.BitRate' % (channel, type) in el:
                    self.current_media_config_mainstream["BitRate"] = rdict['table.Encode[%d].MainFormat[%d].Video.BitRate'      % (channel, type)]
            
            if 'Encode[%d].ExtraFormat[%d]' % (channel, type) in el:
                #print(el)
                if 'Encode[%d].ExtraFormat[%d].Video.Compression' % (channel, type) in el:
                    self.current_media_config_substream["Compression"] = rdict['table.Encode[%d].ExtraFormat[%d].Video.Compression'  % (channel, type)]
                if 'Encode[%d].ExtraFormat[%d].Video.CustomResolutionName' % (channel, type) in el:
                    self.current_media_config_substream["CustomResolutionName"] = rdict['table.Encode[%d].ExtraFormat[%d].Video.CustomResolutionName'   % (channel, type)]
                if 'Encode[%d].ExtraFormat[%d].Video.FPS' % (channel, type) in el:
                    self.current_media_config_substream["FPS"] = rdict['table.Encode[%d].ExtraFormat[%d].Video.FPS'          % (channel, type)]
                if 'Encode[%d].ExtraFormat[%d].Video.Quality' % (channel, type) in el:
                    self.current_media_config_substream["Quality"] = rdict['table.Encode[%d].ExtraFormat[%d].Video.Quality'      % (channel, type)]
                if 'Encode[%d].ExtraFormat[%d].Video.BitRateControl' % (channel, type) in el:
                    self.current_media_config_substream["BitRateControl"] = rdict['table.Encode[%d].ExtraFormat[%d].Video.BitRateControl'      % (channel, type)]
                if 'Encode[%d].ExtraFormat[%d].Video.BitRate' % (channel, type) in el:
                    self.current_media_config_substream["BitRate"] = rdict['table.Encode[%d].ExtraFormat[%d].Video.BitRate'      % (channel, type)]
                if 'Encode[%d].ExtraFormat[%d].VideoEnable' % (channel, type) in el:
                    self.current_media_config_substream["VideoEnable"] = rdict['table.Encode[%d].ExtraFormat[%d].VideoEnable'      % (channel, type)]


        #print("current_media_config_mainstream",self.current_media_config_mainstream)
        return self.current_media_config_mainstream, self.current_media_config_substream
        
        
    
    def setDefaultMediaEncode(self, channel = 0, type = 0, stream = "MainFormat"): 
        Compression = self.default_media_config["Compression"]
        CustomResolutionName = self.default_media_config["CustomResolutionName"]
        FPS     = self.default_media_config["FPS"]
        BitRateControl = self.default_media_config["BitRateControl"]
        Quality = self.default_media_config["Quality"]
        BitRate = self.default_media_config["BitRate"]
        print("SE envia CONFIGURACION >>>> ", FPS)
        self.dvr.SetMediaEncode(channel,type, Compression, CustomResolutionName, FPS, BitRateControl, Quality, BitRate, stream)

    def setLanguage(self):
        Language = self.default_general_config["Language"]
        self.dvr.SetLanguage(Language)
    
    def getLanguage(self):
        language = self.dvr.GetLanguage()
        return language

    def getDeviceType(self):
        print("getDeviceType()")
        rdict = self.dvr.GetDeviceType()
        device_type = rdict['type']  if 'type'  in rdict else ""
        return device_type

    

    def setCurrentTime(self):
        #random_time = "2023-01-19 09:12:00"
        current_time = datetime.now()
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print("Curr ", current_time)
        self.dvr.SetCurrentTime2(current_time)


    def getCurrentTime(self):
        current_time = self.dvr.GetCurrentTime()
        print("Curr ", current_time)
        return current_time
    
    def set_default_config(self):
        print(">> Current Config:",self.GetMediaEncodeConfig(0,0))
        response = self.setDefaultMediaEncode(0,0)
        if response:
            print("Conf Success 200")
        print(">> Current Config:",self.GetMediaEncodeConfig(0,0))

        #self.setDefaultMediaEncode(0,2)
        #self.setDefaultMediaEncode(0,3)
        #self.setDefaultMediaEncode(0,4)
        #self.setDefaultMediaEncode(0,5)
        self.setLanguage()
        self.setCurrentTime()
        print(">> Current Config:",self.GetMediaEncodeConfig(0,0))


def main():
    #print("Dahua config---")
    
    #Media config
    default_media_config = {}
    default_general_config = {}
    default_media_config["Compression"] = "H.264"
    default_media_config["CustomResolutionName"] = "720P"
    default_media_config["SmartCodec"] = "Off"
    default_media_config["FPS"] = 5
    default_media_config["BitRateControl"] = "VBR"
    default_media_config["Quality"] = 4
    default_media_config["BitRate"] = 512

    #General config
    default_general_config["Language"] = "English"

    #Conexion
    host = "elipgomexico.ddns.net"
    port = "elipgomexico.ddns.net"
    user = "test"
    password = "test$2022"
    dvr = Dahua(host, port, user, password)
    config = Config(default_media_config, default_general_config, dvr)
    #config.set_default_config()
    

if __name__ == '__main__':
    main()
