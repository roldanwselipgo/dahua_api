RESOLUTION = {}
RESOLUTION["D1"]                  =    "704x576"
RESOLUTION["HD1"]                 =    "352x576"
RESOLUTION["BCIF"]                =    "704x288"
RESOLUTION["2CIF"]                =    "704x288"
RESOLUTION["CIF"]                 =    "352x288"
RESOLUTION["QCIF"]                =    "176x144"
RESOLUTION["NHD"]                 =    "640x360"
RESOLUTION["VGA"]                 =    "640x480"
RESOLUTION["QVGA"]                =    "320x240"
RESOLUTION["SVCD"]                =    "480x480"
RESOLUTION["QQVGA"]               =    "160x128"
RESOLUTION["SVGA"]                =    "800x592"
RESOLUTION["SVGA1"]               =    "800x600"
RESOLUTION["WVGA"]                =    "800x480"
RESOLUTION["FWVGA"]               =    "854x480"
RESOLUTION["DVGA"]                =    "960x640"
RESOLUTION["XVGA"]                =    "1024x768"
RESOLUTION["WXGA"]                =    "1280x800"
RESOLUTION["WXGA2"]               =    "1280x768"
RESOLUTION["WXGA3"]               =    "1280x854"
RESOLUTION["WXGA4"]               =    "1366x768"
RESOLUTION["SXGA"]                =    "1280x1024"
RESOLUTION["SXGA+"]               =    "1400x1050"
RESOLUTION["WSXGA"]               =    "1600x1024"
RESOLUTION["UXGA"]                =    "1600x1200"
RESOLUTION["WUXGA"]               =    "1920x1200"
RESOLUTION["ND1"]                 =    "240x192"
RESOLUTION["720P"]                =    "1280x720"
RESOLUTION["1080P"]               =    "1920x1080"
RESOLUTION["QFHD"]                =    "3840x2160"

RESOLUTION["1_3M", "1280x960"]    =    "1280x960"
RESOLUTION["2_5M", "1872x1408"]   =    "1872x1408"
RESOLUTION["5M", "3744x1408"]     =    "3744x1408"
RESOLUTION["3M", "2048x1536"]     =    "2048x1536"
RESOLUTION["5_0M", "2432x2048"]   =    "2432x2048"
RESOLUTION["1_2M", "1216x1024"]   =    "1216x1024"
RESOLUTION["5_1M", "2560x1920"]   =    "2560x1920"

RESOLUTION["1408x1024"]           =    "1408x1024"
RESOLUTION["3296x2472"]           =    "3296x2472"
RESOLUTION["960H"]                =    "960x576"
RESOLUTION["DV720P"]              =    "960x720"
RESOLUTION["2560x1600"]           =    "2560x1600"
RESOLUTION["2336x1752"]           =    "2336x1752"
RESOLUTION["2592x2048"]           =    "2592x2048"
RESOLUTION["2448x2048"]           =    "2448x2048"
RESOLUTION["1920x1440"]           =    "1920x1440"
RESOLUTION["2752x2208"]           =    "2752x2208"
RESOLUTION["3840x2160"]           =    "3840x2160"
RESOLUTION["4096x2160"]           =    "4096x2160"
class Resolution():
    def __init__(self):
        pass
    def get_resolution(self,name):
        try:
            resolution = RESOLUTION[name]
            return resolution
        except:
            return name











