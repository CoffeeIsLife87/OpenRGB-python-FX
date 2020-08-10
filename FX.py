import openrgb , time 
from openrgb.utils import DeviceType , RGBColor , ModeData , ModeColors , ModeDirections

import RGBModes

RGBModes.SupportedModes('Corsair Vengeance Pro RGB')

client = openrgb.OpenRGBClient()

client.off()

Dlist = client.devices

for Device in client.devices: #for some devices static = direct
    print(Device)
   #if Device.name == 'Corsair Vengeance Pro RGB':
   #        Device.set_mode('Direct')
    time.sleep(0.25)

def SetDeviceColors(R , G , B):#device , led , R , G , B):
    for i in Dlist:
        i.set_color(RGBColor(R,G,B))
        time.sleep(0.0003)

def DebugRGB(R , G , B):
    Debug = 1
    if Debug == 1:
        print(R , G , B)
    else:
        return

def SpectrumCycle():
    R = G = B = 0
    RedoLoop = 0
    while 1 == 1:
        if RedoLoop == 1:
            RedoLoop = 0
        R += 1
        DebugRGB(R , G , B)
        SetDeviceColors(R , G , B)
        time.sleep(0.001)
        if R == 255:
            while 1 == 1:
                if RedoLoop == 1:
                    break
                G += 1
                DebugRGB(R , G , B)
                SetDeviceColors(R , G , B)
                time.sleep(0.001)
                if G == 255:
                    while 1 == 1:
                        if RedoLoop == 1:
                            break
                        R -= 1
                        DebugRGB(R , G , B)
                        SetDeviceColors(R , G , B)
                        time.sleep(0.001)
                        if R == 0:
                            while 1 == 1:
                                if RedoLoop == 1:
                                    break
                                B += 1
                                DebugRGB(R , G , B)
                                SetDeviceColors(R , G , B)
                                time.sleep(0.001)
                                if B == 255:
                                    while 1 == 1:
                                        if RedoLoop == 1:
                                            break
                                        G -= 1
                                        DebugRGB(R , G , B)
                                        SetDeviceColors(R , G , B)
                                        time.sleep(0.001)
                                        if G == 0:
                                            while 1 == 1:
                                                if RedoLoop == 1:
                                                    break
                                                R += 1
                                                DebugRGB(R , G , B)
                                                SetDeviceColors(R , G , B)
                                                time.sleep(0.001)
                                                if R == 255:
                                                    while 1 == 1:
                                                        if RedoLoop == 1:
                                                            break
                                                        B -= 1
                                                        DebugRGB(R , G , B)
                                                        SetDeviceColors(R , G , B)
                                                        time.sleep(0.001)
                                                        if B == 0:
                                                            while 1 == 1:
                                                                if RedoLoop == 1:
                                                                    break
                                                                G += 1
                                                                B += 1
                                                                DebugRGB(R , G , B)
                                                                SetDeviceColors(R , G , B)
                                                                time.sleep(0.001)
                                                                if (str(R) + str(G) + str(B)) == "255255255":
                                                                    while 1 == 1:
                                                                        R -= 1
                                                                        G -= 1
                                                                        B -= 1
                                                                        DebugRGB(R , G , B)
                                                                        SetDeviceColors(R , G , B)
                                                                        time.sleep(0.001)
                                                                        if B == 0:
                                                                            RedoLoop = 1
                                                                            break

def Rainbow():
    for Device in Dlist:
        if Device.name == 'Corsair Vengeance Pro RGB':
            Device.set_mode('rainbow wave')
        else:
            Device.set_mode('rainbow')
#Rainbow()
#SpectrumCycle()