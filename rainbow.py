import openrgb
from openrgb.utils import RGBColor

client = openrgb.OpenRGBClient()
Dlist = client.devices

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
        print('loop finished')
                                                            
P1()

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
     #           print(Offset)
            num += 1
    #print(Zones[0])
    #print([i[2] for i in Zones])

ZoneDef()

def setColors(ColorBase):
    global Offset
    #while True:
    print(Zones[0][2][1])
    for Z in Zones[0]:
        print(len(Z))
        #for i in Z:
        #    print(i)
            
        #LED = Zone
        #print(LED)
                    #SplitZone = len(zone.leds)
                    #Color = len(CBase)/SplitZone
                    #LEDColor = (int(Color)*Offset)
                    #if LEDColor >= len(ColorBase):
                    #    LEDColor = len(ColorBase) -1
                    #CR , CB , CG = ColorBase[LEDColor]
                    #led.set_color(RGBColor(CR , CB , CG))
                    #Offset += 1

C = CBase

setColors(ColorBase=C)
