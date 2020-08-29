import openrgb , time
from openrgb.utils import RGBColor
import numpy as np


client = openrgb.OpenRGBClient()
Dlist = client.devices

def wait():
    time.sleep(0.003)

def SetStatic():
    for Device in Dlist:
        try:
            Device.set_mode('static')
        except:
            Device.set_mode('direct')

#LEDList = []
#for LED in Device.leds:
#    LEDList = LEDList + [LED]

NumList = [0]
FormList = 1
while NumList[-1] != 100:
    NumList = NumList + [FormList]
    FormList += 1

def CustomSpectrumCycle(CycleSpeed=3):
    SetStatic()
    R = G = B = 0
    RedoLoop = 0
    while 1 == 1:
        if RedoLoop == 1:
            RedoLoop = 0
        R += CycleSpeed
        DebugRGB(R , G , B)
        SetDeviceColors('all' , R , G , B)
        time.sleep(0.002)
        if R == 255:
            while 1 == 1:
                if RedoLoop == 1:
                    break
                G += CycleSpeed
                DebugRGB(R , G , B)
                SetDeviceColors('all' , R , G , B)
                time.sleep(0.002)
                if G == 255:
                    while 1 == 1:
                        if RedoLoop == 1:
                            break
                        R -= CycleSpeed
                        DebugRGB(R , G , B)
                        SetDeviceColors('all' , R , G , B)
                        time.sleep(0.002)
                        if R == 0:
                            while 1 == 1:
                                if RedoLoop == 1:
                                    break
                                B += CycleSpeed
                                DebugRGB(R , G , B)
                                SetDeviceColors('all' , R , G , B)
                                time.sleep(0.002)
                                if B == 255:
                                    while 1 == 1:
                                        if RedoLoop == 1:
                                            break
                                        G -= CycleSpeed
                                        DebugRGB(R , G , B)
                                        SetDeviceColors('all' , R , G , B)
                                        time.sleep(0.002)
                                        if G == 0:
                                            while 1 == 1:
                                                if RedoLoop == 1:
                                                    break
                                                R += CycleSpeed
                                                DebugRGB(R , G , B)
                                                SetDeviceColors('all' , R , G , B)
                                                time.sleep(0.002)
                                                if R == 255:
                                                    while 1 == 1:
                                                        if RedoLoop == 1:
                                                            break
                                                        B -= CycleSpeed
                                                        DebugRGB(R , G , B)
                                                        SetDeviceColors('all' , R , G , B)
                                                        time.sleep(0.002)
                                                        if B == 0:
                                                            while 1 == 1:
                                                                if RedoLoop == 1:
                                                                    break
                                                                G += CycleSpeed
                                                                B += CycleSpeed
                                                                DebugRGB(R , G , B)
                                                                SetDeviceColors('all' , R , G , B)
                                                                time.sleep(0.002)
                                                                if (str(R) + str(G) + str(B)) == "255255255":
                                                                    while 1 == 1:
                                                                        R -= CycleSpeed
                                                                        G -= CycleSpeed
                                                                        B -= CycleSpeed
                                                                        DebugRGB(R , G , B)
                                                                        SetDeviceColors('all' , R , G , B)
                                                                        time.sleep(0.002)
                                                                        if B == 0:
                                                                            RedoLoop = 1
                                                                            break

rb = [(255,0,0),(255,100,0),(255,255,0),(150,255,0),(0,255,0),(0,255,255),(0,0,255),(150,0,255),(255,0,255)]
red = rb[0]
orange = rb[1]
yellow = rb[2]
lime = rb[3]
green = rb[4]
cyan = rb[5]
blue = rb[6]
purple = rb[7]
pink = rb[8]

#print(len(rb))

DMap = [] #this will become an array using the following while loop
SetX = 0

while SetX <= 20:
    SetX += 1
    SetY = 0
    while SetY <= 20:
        SetY += 1
        DMap = DMap + [0]
    if SetY == 80:
        DMap = DMap + '\n'

Dmap = np.zeros((20,20),int)
print(Dmap)


n=20
Grid = [0] * n
for i in range(n):
    Grid[i] = [0] * n

def Rainbow():
    while True:
        for i in NumList:
            for Device in Dlist:
                try:
                    Device.leds[i].set_color(RGBColor(0,0,255))
                    time.sleep(0.5)
                except:
                    pass