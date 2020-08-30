#I was using this to create the effect
#this has no use other than that but I will leave it in anyways

import openrgb , time
from openrgb.utils import RGBColor

client = openrgb.OpenRGBClient()
Dlist = client.devices

def OneFunc(speed=3):
    
    Offset = 1
    def P1(CycleSpeed=15):#you must be able to devide 255 by CycleSpeed or THIS WILL NOT WORK
        CBase = []
        R = G = B = 0
        while 1 == 1:
            R += CycleSpeed
            CBase = CBase + [(R,G,B)]
            if R == 255:
                while 1 == 1:
                    G += CycleSpeed
                    CBase = CBase + [(R,G,B)]
                    if G == 255:
                        while 1 == 1:
                            R -= CycleSpeed
                            CBase = CBase + [(R,G,B)]
                            if R == 0:
                                while 1 == 1:
                                    B += CycleSpeed
                                    CBase = CBase + [(R,G,B)]
                                    if B == 255:
                                        while 1 == 1:
                                            G -= CycleSpeed
                                            CBase = CBase + [(R,G,B)]
                                            if G == 0:
                                                while 1 == 1:
                                                    R += CycleSpeed
                                                    CBase = CBase + [(R,G,B)]
                                                    if R == 255:
                                                        while 1 == 1:
                                                            B -= CycleSpeed
                                                            CBase = CBase + [(R,G,B)]
                                                            #print(CBase)
                                                            if B == 0:
                                                                return CBase
    CB = P1()

    CBase = CB

    def wait():
        time.sleep(float('0.00%d'%speed))
    
    Zones = []
    num = 0
    
    for device in Dlist:
        for zone in device.zones:
            Zones = Zones + [[zone]]
            Offset = 1
            for led in zone.leds:
                Zones[num] = Zones[num] + [[[led],[Offset]]]
                Offset += 1
            num += 1
    
    while True:
        wait()
        for Z in Zones:
            CheckVal = len(Z) -1
            for LED in Z[1:-1]:
                Color = len(CBase)/CheckVal
                LEDColor = (int(Color)*LED[1][0])
                if LEDColor >= len(CBase):
                    LEDColor = len(CBase) -1
                CR , CB , CG = CBase[LEDColor]
                LED[0][0].set_color(RGBColor(CR , CB , CG))
                if LED[1][0] >= CheckVal:
                    LED[1][0] = 1
                else:
                    LED[1][0] += 1

OneFunc()
exit()


CBase = []

Offset = 1

def MakeColorBase(R,G,B):
    global CBase
    CBase = CBase + [(R,G,B)]

def P1(CycleSpeed=15):#
    try:
        R = G = B = 0
        while 1 == 1:
            R += CycleSpeed
            MakeColorBase(R,G,B)
            if R == 255:
                while 1 == 1:
                    G += CycleSpeed
                    MakeColorBase(R , G , B)
                    if G == 255:
                        while 1 == 1:
                            R -= CycleSpeed
                            MakeColorBase(R , G , B)
                            if R == 0:
                                while 1 == 1:
                                    B += CycleSpeed
                                    MakeColorBase(R , G , B)
                                    if B == 255:
                                        while 1 == 1:
                                            G -= CycleSpeed
                                            MakeColorBase(R , G , B)
                                            if G == 0:
                                                while 1 == 1:
                                                    R += CycleSpeed
                                                    MakeColorBase(R , G , B)
                                                    if R == 255:
                                                        while 1 == 1:
                                                            B -= CycleSpeed
                                                            MakeColorBase(R , G , B)
                                                            if B == 0:
                                                                print(X)
    except:
        pass
        #print('loop finished')
                                                            
P1()

def wait():
    time.sleep(0.05)

Zones = []
num = 0

def ZoneDef():
    global Zones , num
    for device in Dlist:
        for zone in device.zones:
            Zones = Zones + [[zone]]
            Offset = 1
            for led in zone.leds:
                Zones[num] = Zones[num] + [[[led],[Offset]]]
                Offset += 1
            num += 1

ZoneDef()

def setColors(ColorBase):
    global Offset
    while True:
        wait()
        for Z in Zones:
            CheckVal = len(Z) -1
            for LED in Z[1:-1]:
                Color = len(CBase)/CheckVal
                LEDColor = (int(Color)*LED[1][0])
                if LEDColor >= len(ColorBase):
                    LEDColor = len(ColorBase) -1
                CR , CB , CG = ColorBase[LEDColor]
                LED[0][0].set_color(RGBColor(CR , CB , CG))
                if LED[1][0] >= CheckVal:
                    LED[1][0] = 1
                else:
                    LED[1][0] += 1

C = CBase

setColors(ColorBase=C)
