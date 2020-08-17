import openrgb , time , RGBModes , string
import tkinter as tk
from openrgb.utils import DeviceType , RGBColor , ModeData
from LightIndexes import GetIndex


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
    Debug = 1
    if Debug == 1:
        print(R , G , B)
    else:
        return

def SpectrumCycle():
    for Device in Dlist:
        Device.set_mode(RGBModes.SupportedModes(Device.name , 'cycling'))
        wait()

def Rainbow():
    for Device in Dlist:
        #print(Device)
        #print(RGBModes.SupportedModes(Device.name , 'rainbow'))
        for mode in Device.modes:
            #print(mode.name.lower())
            #exit()
        #exit()
            if mode.name.lower() == RGBModes.SupportedModes(Device.name , 'rainbow'):
                #mode.speed = 2
                Device.set_mode(mode)
        wait()

def CustomSpectrumCycle(CycleSpeed=''):
    SetMode('static')
    CycleSpeed = 3
    R = G = B = 0
    RedoLoop = 0
    while 1 == 1:
        if RedoLoop == 1:
            RedoLoop = 0
        R += CycleSpeed
        DebugRGB(R , G , B)
        SetDeviceColors(R , G , B)
        time.sleep(0.002)
        if R == 255:
            while 1 == 1:
                if RedoLoop == 1:
                    break
                G += CycleSpeed
                DebugRGB(R , G , B)
                SetDeviceColors(R , G , B)
                time.sleep(0.002)
                if G == 255:
                    while 1 == 1:
                        if RedoLoop == 1:
                            break
                        R -= CycleSpeed
                        DebugRGB(R , G , B)
                        SetDeviceColors(R , G , B)
                        time.sleep(0.002)
                        if R == 0:
                            while 1 == 1:
                                if RedoLoop == 1:
                                    break
                                B += CycleSpeed
                                DebugRGB(R , G , B)
                                SetDeviceColors(R , G , B)
                                time.sleep(0.002)
                                if B == 255:
                                    while 1 == 1:
                                        if RedoLoop == 1:
                                            break
                                        G -= CycleSpeed
                                        DebugRGB(R , G , B)
                                        SetDeviceColors(R , G , B)
                                        time.sleep(0.002)
                                        if G == 0:
                                            while 1 == 1:
                                                if RedoLoop == 1:
                                                    break
                                                R += CycleSpeed
                                                DebugRGB(R , G , B)
                                                SetDeviceColors(R , G , B)
                                                time.sleep(0.002)
                                                if R == 255:
                                                    while 1 == 1:
                                                        if RedoLoop == 1:
                                                            break
                                                        B -= CycleSpeed
                                                        DebugRGB(R , G , B)
                                                        SetDeviceColors(R , G , B)
                                                        time.sleep(0.002)
                                                        if B == 0:
                                                            while 1 == 1:
                                                                if RedoLoop == 1:
                                                                    break
                                                                G += CycleSpeed
                                                                B += CycleSpeed
                                                                DebugRGB(R , G , B)
                                                                SetDeviceColors(R , G , B)
                                                                time.sleep(0.002)
                                                                if (str(R) + str(G) + str(B)) == "255255255":
                                                                    while 1 == 1:
                                                                        R -= CycleSpeed
                                                                        G -= CycleSpeed
                                                                        B -= CycleSpeed
                                                                        DebugRGB(R , G , B)
                                                                        SetDeviceColors(R , G , B)
                                                                        time.sleep(0.002)
                                                                        if B == 0:
                                                                            RedoLoop = 1
                                                                            break

def SetMode(Mode):
    for Device in client.devices:
        if Device.name != 'ASRock Polychrome FW 3.255':
            try:
                Device.set_mode(RGBModes.SupportedModes(Device.name,Mode))
            except:
                print('Unable to set %s'%Device.name)
            
#GUI()
#ram is left to right (0 to 1 to 2 and so forth)

#for Device in client.devices:
#    Device.set_mode(RGBModes.SupportedModes(Device.name,'cycling'))
#    #print(GetIndex.Index(Device.name))

#    Device.set_mode(RGBModes.SupportedModes(Device.name , 'static'))
#    wait()
