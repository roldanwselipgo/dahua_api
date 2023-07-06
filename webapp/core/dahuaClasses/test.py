from dahuaClasses.dahua_class import Dahua

# Create your tests here.
day="12/04/23"
starttime = f"{day}%2000:00:00"
endtime = f"{day}%2023:00:00"
print("...",starttime,endtime)
#print("Today is: ", today, yesterday, type(today))
#return 0
if 1:
    dvr = Dahua("192.169.26.2", 80, "admin", "Elipgo$123")
    by_channels = []

    file = open('result_segmentos.csv','a+')
    print("abvr")
    dvr.MediaFindFileCreate() 
    if 1:
        rsp = dvr.MediaFindFile(-1, starttime, endtime)
        var = 2
        segmentos = []
        while (var):
            rdict = dvr.MediaFindNextFile(100)
            if rdict!=-1:
                print(rdict)
            else:
                var = 0