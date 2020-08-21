import time , openrgb

client = openrgb.OpenRGBClient()

Dlist = client.devices

def SetDeviceColors(R , G , B):#device , led , R , G , B):
    for i in Dlist:
        if i.name != 'ASRock Polychrome FW 3.255':
            #print(i.id)
            i.set_color(RGBColor(R,G,B) , fast='true')
            time.sleep(0.0003)

def wait():
    time.sleep(0.003)

def DebugRGB(R , G , B):# for printing the values that are being set
    Debug = 0
    if Debug == 1:
        print(R , G , B)
    else:
        return