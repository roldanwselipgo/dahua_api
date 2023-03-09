#from dahua_class import Dahua
from .dahua_class import Dahua

from datetime import datetime
from .resolutions import Resolution


class Config():
    def __init__(self, default_media_config = {}, default_general_config = {} , dvr = None ):
        self.dvr = dvr
        self.current_media_config_mainstream = {}
        self.current_media_config_substream = {}
        self.default_media_config = default_media_config
        self.default_general_config = default_general_config
        self.resolution = Resolution()

    def ChannelCount(self):
        rdict = self.dvr.GetMediaEncode() 
        channels = 0
        for el in rdict:
            if 'Encode[%d]' % (channels) in el:
                channels = channels + 1
        print("Channels: ",channels)
        return channels
            
    def ChannelDetect(self):
        channels = []
        rdict = self.dvr.GetMediaEncode() 
        for el in rdict:
            for i in range(0,50):
                if 'Encode[%d]' % (i) in el:
                    if i not in channels:
                        channels.append(i)
                    break
            
        print("Channels>>>:",channels)
        return channels

    def GetAllMediaEncodeConfig(self, channel = 0, type = 0):
        rdict = self.dvr.GetMediaEncode()
        return rdict

    def GetMediaEncodeConfigCapability(self, channels = 0, type = 0):
        rdict = self.dvr.GetMediaEncode()
        rdict_caps = self.dvr.GetConfigCaps()
        #print("Capability: ",rdict_caps)
        #Conteo canales
        channels = []
        for el in rdict:
            for i in range(0,50):
                if 'Encode[%d]' % (i) in el:
                    if i not in channels:
                        channels.append(i)
                    break
        print("Channels: ",channels)
        #Recorrer informacion por canal
        result = []
        
        for channel in channels:
            configs = []
            self.current_media_config_mainstream={}
            self.current_media_config_substream={}
            #Inicializar Mainstream
            self.current_media_config_mainstream["Channel"] = None
            self.current_media_config_mainstream["Stream"] = ["MainFormat"]
            self.current_media_config_mainstream["Compression"] = []
            self.current_media_config_mainstream["resolution"] = []
            self.current_media_config_mainstream["FPS"] = []
            self.current_media_config_mainstream["Quality"] = None
            self.current_media_config_mainstream["BitRateControl"] = []
            self.current_media_config_mainstream["BitRate"] = []
            #Inicializar Substream
            self.current_media_config_substream["Channel"] = None
            self.current_media_config_substream["Stream"] = ["ExtraFormat"]
            self.current_media_config_substream["Compression"] = []
            self.current_media_config_substream["resolution"] = []
            self.current_media_config_substream["FPS"] = []
            self.current_media_config_substream["Quality"] = None
            self.current_media_config_substream["BitRateControl"] = []
            self.current_media_config_substream["BitRate"] = []
            self.current_media_config_substream["VideoEnable"] = None
            for el in rdict:
                #print(el, rdict[el])
                if 'Encode[%d].MainFormat[%d]' % (channel, type) in el:
                    #print(el)
                    if 'Encode[%d].MainFormat[%d].Video.Compression' % (channel, type) in el:
                        prof="Main"
                        for el in rdict:
                            if 'Encode[%d].MainFormat[%d].Video.Profile' % (channel, type) in el:
                                prof = rdict['table.Encode[%d].MainFormat[%d].Video.Profile'  % (channel, type)]
                        self.current_media_config_mainstream["Compression"].append(rdict['table.Encode[%d].MainFormat[%d].Video.Compression'  % (channel, type)] + " "+prof)
                        for caps in rdict_caps:
                            if 'caps[%d].MainFormat[%d].Video.CompressionTypes' % (channel, type) in caps:
                                options = rdict_caps['caps[%d].MainFormat[%d].Video.CompressionTypes'  % (channel, type)].split(",")
                                if len(options) > 1:
                                    for profile_index in range(0,3): #Busca los 3 perfiles (main, baseline, high):
                                        for caps2 in rdict_caps:
                                            if 'caps[%d].MainFormat[%d].Video.H264Profile[%d]' % (channel, type, profile_index) in caps2:
                                                profile= rdict_caps['caps[%d].MainFormat[%d].Video.H264Profile[%d]' % (channel, type, profile_index)]
                                                for option in options : 
                                                    if option == "H.264": self.current_media_config_mainstream["Compression"].append(option+" "+profile)  
                                                    else:
                                                        if option not in self.current_media_config_mainstream["Compression"]: 
                                                            self.current_media_config_mainstream["Compression"].append(option) 
                                                     

                    if 'Encode[%d].MainFormat[%d].Video.resolution' % (channel, type) in el:
                        self.current_media_config_mainstream["resolution"].append(rdict['table.Encode[%d].MainFormat[%d].Video.resolution'   % (channel, type)])
                        for caps in rdict_caps:
                            if 'caps[%d].MainFormat[%d].Video.ResolutionTypes' % (channel, type) in caps:
                                options = rdict_caps['caps[%d].MainFormat[%d].Video.ResolutionTypes'  % (channel, type)].split(",")
                                #print("options",options)
                                if len(options) > 1:
                                    for option in options: 
                                        option = self.resolution.get_resolution(option)
                                        self.current_media_config_mainstream["resolution"].append(option) 

                    if 'Encode[%d].MainFormat[%d].Video.FPS' % (channel, type) in el:
                        self.current_media_config_mainstream["FPS"].append(rdict['table.Encode[%d].MainFormat[%d].Video.FPS'          % (channel, type)])
                        for caps in rdict_caps:
                            if 'caps[%d].MainFormat[%d].Video.FPSMax' % (channel, type) in caps:
                                options = rdict_caps['caps[%d].MainFormat[%d].Video.FPSMax'  % (channel, type)]
                                options = range(int(options))
                                if len(options) > 1:
                                    for option in options : self.current_media_config_mainstream["FPS"].append(option) 

                    if 'Encode[%d].MainFormat[%d].Video.Quality' % (channel, type) in el:
                        self.current_media_config_mainstream["Quality"] = rdict['table.Encode[%d].MainFormat[%d].Video.Quality'      % (channel, type)] , 0
                    if 'Encode[%d].MainFormat[%d].Video.BitRateControl' % (channel, type) in el:
                        self.current_media_config_mainstream["BitRateControl"].append(rdict['table.Encode[%d].MainFormat[%d].Video.BitRateControl'      % (channel, type)])
                        options = ["CBR", "VBR"]
                        for option in options:
                            self.current_media_config_mainstream["BitRateControl"].append(option) if option not in self.current_media_config_mainstream["BitRateControl"] else 0

                    if 'Encode[%d].MainFormat[%d].Video.BitRate' % (channel, type) in el:
                        if rdict['table.Encode[%d].MainFormat[%d].Video.BitRate'      % (channel, type)] not in self.current_media_config_mainstream["BitRate"]:
                            self.current_media_config_mainstream["BitRate"].append(rdict['table.Encode[%d].MainFormat[%d].Video.BitRate'      % (channel, type)])
                        for caps in rdict_caps:
                            if 'caps[%d].MainFormat[%d].Video.BitRateOptions' % (channel, type) in caps:
                                options = rdict_caps['caps[%d].MainFormat[%d].Video.BitRateOptions'  % (channel, type)].split(",")
                                if len(options) > 1:
                                   for value in range(int(options[0]),int(options[1])):
                                       if value % int(options[0]) == 0:
                                           self.current_media_config_mainstream["BitRate"].append(value) if value not in self.current_media_config_mainstream["BitRate"] else 0
                                 
                
                if 'Encode[%d].ExtraFormat[%d]' % (channel, type) in el:
                    if 'Encode[%d].ExtraFormat[%d].Video.Compression' % (channel, type) in el:
                        prof = "Main"
                        for el in rdict:
                            if 'Encode[%d].ExtraFormat[%d].Video.Profile' % (channel, type) in el:
                                prof = rdict['table.Encode[%d].ExtraFormat[%d].Video.Profile'  % (channel, type)]
                        self.current_media_config_substream["Compression"].append(rdict['table.Encode[%d].ExtraFormat[%d].Video.Compression'  % (channel, type)] + " "+prof)
                        for caps in rdict_caps:
                            if 'caps[%d].ExtraFormat[%d].Video.CompressionTypes' % (channel, type) in caps:
                                options = rdict_caps['caps[%d].ExtraFormat[%d].Video.CompressionTypes'  % (channel, type)].split(",")
                                if len(options) > 1:
                                    for profile_index in range(0,3): #Busca los 3 perfiles (main, baseline, high):
                                        for caps2 in rdict_caps:
                                            if 'caps[%d].ExtraFormat[%d].Video.H264Profile[%d]' % (channel, type, profile_index) in caps2:
                                                profile= rdict_caps['caps[%d].ExtraFormat[%d].Video.H264Profile[%d]' % (channel, type, profile_index)]
                                                for option in options : 
                                                    if option == "H.264": self.current_media_config_substream["Compression"].append(option+" "+profile)  
                                                    else:
                                                        if option not in self.current_media_config_substream["Compression"]:
                                                            self.current_media_config_substream["Compression"].append(option)

                    if 'Encode[%d].ExtraFormat[%d].Video.resolution' % (channel, type) in el:
                        self.current_media_config_substream["resolution"].append(rdict['table.Encode[%d].ExtraFormat[%d].Video.resolution'   % (channel, type)])
                        for caps in rdict_caps:
                            if 'caps[%d].ExtraFormat[%d].Video.ResolutionTypes' % (channel, type) in caps:
                                options = rdict_caps['caps[%d].ExtraFormat[%d].Video.ResolutionTypes'  % (channel, type)].split(",")
                                if len(options) > 1:
                                    for option in options: 
                                        option = self.resolution.get_resolution(option)
                                        self.current_media_config_substream["resolution"].append(option) 

                    if 'Encode[%d].ExtraFormat[%d].Video.FPS' % (channel, type) in el:
                        self.current_media_config_substream["FPS"].append(rdict['table.Encode[%d].ExtraFormat[%d].Video.FPS'          % (channel, type)])
                        for caps in rdict_caps:
                            if 'caps[%d].ExtraFormat[%d].Video.FPSMax' % (channel, type) in caps:
                                options = rdict_caps['caps[%d].ExtraFormat[%d].Video.FPSMax'  % (channel, type)]
                                options = range(int(options))
                                #print("FPS MAX: ",options)
                                if len(options) > 1:
                                    for option in options : self.current_media_config_substream["FPS"].append(option)

                    if 'Encode[%d].ExtraFormat[%d].Video.Quality' % (channel, type) in el:
                        self.current_media_config_substream["Quality"] = rdict['table.Encode[%d].ExtraFormat[%d].Video.Quality'      % (channel, type)], 0
                    if 'Encode[%d].ExtraFormat[%d].Video.BitRateControl' % (channel, type) in el:
                        self.current_media_config_substream["BitRateControl"].append(rdict['table.Encode[%d].ExtraFormat[%d].Video.BitRateControl'      % (channel, type)])
                        options = ["CBR", "VBR"]
                        for option in options:
                            self.current_media_config_substream["BitRateControl"].append(option) if option not in self.current_media_config_substream["BitRateControl"] else 0
                    if 'Encode[%d].ExtraFormat[%d].Video.BitRate' % (channel, type) in el:
                        if rdict['table.Encode[%d].ExtraFormat[%d].Video.BitRate'      % (channel, type)] not in self.current_media_config_substream["BitRate"]:
                            self.current_media_config_substream["BitRate"].append(rdict['table.Encode[%d].ExtraFormat[%d].Video.BitRate'      % (channel, type)])
                        for caps in rdict_caps:
                            if 'caps[%d].ExtraFormat[%d].Video.BitRateOptions' % (channel, type) in caps:
                                options = rdict_caps['caps[%d].ExtraFormat[%d].Video.BitRateOptions'  % (channel, type)].split(",")
                                if len(options) > 1:
                                    for value in range(int(options[0]),int(options[1])):
                                        if value % int(options[0]) == 0:
                                            self.current_media_config_substream["BitRate"].append(value) if value not in self.current_media_config_substream["BitRate"] else 0
                                            
                    if 'Encode[%d].ExtraFormat[%d].VideoEnable' % (channel, type) in el:
                        self.current_media_config_substream["VideoEnable"] = rdict['table.Encode[%d].ExtraFormat[%d].VideoEnable'      % (channel, type)], 0
            self.current_media_config_mainstream["Channel"] = channel, 0
            self.current_media_config_substream["Channel"] = channel, 0
            
            configs.append(self.current_media_config_mainstream)
            configs.append(self.current_media_config_substream)
            result.append(configs)
        #print(self.current_media_config_mainstream, channel)
        #print(self.current_media_config_substream, channel)
        #print("current_media_config_mainstream",self.current_media_config_mainstream)
        return result


    def GetMediaEncodeConfig(self, channels = 0, type = 0):
        rdict = self.dvr.GetMediaEncode()
        #Conteo canales
        channels = []
        for el in rdict:
            for i in range(0,50):
                if 'Encode[%d]' % (i) in el:
                    if i not in channels:
                        channels.append(i)
                    break
        print("Channels: ",channels)
        #Recorrer informacion por canal
        result = []
        
        for channel in channels:
            configs = []
            self.current_media_config_mainstream={}
            self.current_media_config_substream={}
            #Inicializar Mainstream
            self.current_media_config_mainstream["Channel"] = None
            self.current_media_config_mainstream["Stream"] = "MainFormat"
            self.current_media_config_mainstream["Compression"] = None
            self.current_media_config_mainstream["resolution"] = None
            self.current_media_config_mainstream["FPS"] = None
            self.current_media_config_mainstream["Quality"] = None
            self.current_media_config_mainstream["BitRateControl"] = None
            self.current_media_config_mainstream["BitRate"] = None
            #Inicializar Substream
            self.current_media_config_substream["Channel"] = None
            self.current_media_config_substream["Stream"] = "ExtraFormat"
            self.current_media_config_substream["Compression"] = None
            self.current_media_config_substream["resolution"] = None
            self.current_media_config_substream["FPS"] = None
            self.current_media_config_substream["Quality"] = None
            self.current_media_config_substream["BitRateControl"] = None
            self.current_media_config_substream["BitRate"] = None
            self.current_media_config_substream["VideoEnable"] = None
            for el in rdict:
                #print(el, rdict[el])
                if 'Encode[%d].MainFormat[%d]' % (channel, type) in el:
                    #print(el)
                    if 'Encode[%d].MainFormat[%d].Video.Compression' % (channel, type) in el:
                        self.current_media_config_mainstream["Compression"] = rdict['table.Encode[%d].MainFormat[%d].Video.Compression'  % (channel, type)] 
                    if 'Encode[%d].MainFormat[%d].Video.resolution' % (channel, type) in el:
                        self.current_media_config_mainstream["resolution"] = rdict['table.Encode[%d].MainFormat[%d].Video.resolution'   % (channel, type)]
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
                    if 'Encode[%d].ExtraFormat[%d].Video.resolution' % (channel, type) in el:
                        self.current_media_config_substream["resolution"] = rdict['table.Encode[%d].ExtraFormat[%d].Video.resolution'   % (channel, type)]
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
            self.current_media_config_mainstream["Channel"] = channel
            self.current_media_config_substream["Channel"] = channel
            
            configs.append(self.current_media_config_mainstream)
            configs.append(self.current_media_config_substream)
            result.append(configs)
        #print(self.current_media_config_mainstream, channel)
        #print(self.current_media_config_substream, channel)
        #print("current_media_config_mainstream",self.current_media_config_mainstream)
        return result
        
        
    
    def setDefaultMediaEncode(self, channel = 0, type = 0, stream = "MainFormat"): 
        Compression = self.default_media_config["Compression"]
        resolution = self.default_media_config["resolution"]
        FPS     = self.default_media_config["FPS"]
        BitRateControl = self.default_media_config["BitRateControl"]
        Quality = self.default_media_config["Quality"]
        BitRate = self.default_media_config["BitRate"]
        #if substream
        VideoEnable = self.default_media_config["VideoEnable"]
        print("SE envia CONFIGURACION >>>> ", VideoEnable)
        Profile = "Main"
        values = Compression.split(" ")
        if len(values) == 2:
            Compression = values[0]
            Profile = values[1]

        if stream=="ExtraFormat":
            resolution="640x480" #VGA for substream 
        
        response = self.dvr.SetMediaEncode(channel,type, Compression, resolution, FPS, BitRateControl, Quality, BitRate, VideoEnable, stream, Profile)
        return response

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

    def getHDDevInfo(self):
        rdict =  self.dvr.GetHDDevInfo()
        storage = {}
        storages = []
        for index in range(0,10):
            try:
                storage={}
                storage['Path']=rdict['list.info[0].Detail[%s].Path' % (index)]  if rdict['list.info[0].Detail[%s].Path' % (index)] else 0
                storage['isError']=rdict['list.info[0].Detail[%s].IsError' % (index)]  if rdict['list.info[0].Detail[%s].IsError' % (index)] else 0
                storage['Total']=rdict['list.info[0].Detail[%s].TotalBytes' % (index)]  if rdict['list.info[0].Detail[%s].TotalBytes' % (index)] else 0
                storage['Type']=rdict['list.info[0].Detail[%s].Type' % (index)]  if rdict['list.info[0].Detail[%s].Type' % (index)] else 0
                storage['Used']=rdict['list.info[0].Detail[%s].UsedBytes' % (index)]  if rdict['list.info[0].Detail[%s].UsedBytes' % (index)] else 0
                storage["Total"] = str(int(float(storage["Total"])/1000000000)) + " GB"
                storage["Used"] = str(int(float(storage["Used"])/1000000000)) + " GB"
                storages.append(storage)
            except:
                pass
        #print("storages: ",storages)
        return storages


    

    def setCurrentTime(self, time=None):
        #random_time = "2023-01-19 09:12:00"
        if time:
            self.dvr.SetCurrentTime2(time)
        else:
            current_time = datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            print("Curr ", current_time)
            self.dvr.SetCurrentTime2(current_time)


    def getCurrentTime(self):
        current_time = self.dvr.GetCurrentTime()
        print("Curre ", current_time)
        return current_time
    
    def set_default_config(self):
        print(">> Current Config:",self.GetMediaEncodeConfig(0,0))
        response = self.setDefaultMediaEncode(0,0)
        if response:
            print("Conf Success 200")
        print(">> Current Config:",self.GetMediaEncodeConfig(0,0))
        self.setLanguage()
        self.setCurrentTime()
        print(">> Current Config:",self.GetMediaEncodeConfig(0,0))
