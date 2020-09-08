import openrgb , time , string , colorsys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

def CustomRainbow(speed=1,MaxOffset=30): #Higher = slower
    
    for Device in Dlist:# set to direct or static as a fallback
        time.sleep(0.3)
        try:
            Device.set_mode('direct')
            print('Set %s successfully'%Device.name)
        except:
            try:
                print('error setting %s\nfalling back to static'%Device.name)
                Device.set_mode('static')
            except:
                print("Critical error! couldn't set %s to static or direct"%Device.name)
            
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
        time.sleep(float('0.0%d'%speed))
    
    Zones = []
    num = 0

    for device in Dlist:
        for zone in device.zones:
            Zones = Zones + [[zone]]
            Offset = 2

            if zone.type == ZoneType.ZONE_TYPE_MATRIX:
                for SubZone in zone.matrix_map:
                    for led in SubZone:
                        if led != None:
                            Zones[num] = Zones[num] + [[[device.leds[led]], [Offset]]]

                    Offset += 1
            elif device.name == 'ASRock Polychrome V2':
                for led in reversed(zone.leds):
                    if len(zone.leds) == 1:
                        Offset = 5
                    Zones[num] = Zones[num] + [[[led],[Offset]]]
                    Offset += 1
                    
            else:
                for led in zone.leds:
                    Zones[num] = Zones[num] + [[[led],[Offset]]]
                    Offset += 1
            num += 1

    while True:
        wait()
        for Z in Zones:
            for LED in Z[1:]:
                Color = len(CBase)/MaxOffset
                try:
                    LEDColor = (int(Color)*LED[1][0])
                except:
                    print(LED)
                    exit()
                if LEDColor >= len(CBase):
                    LEDColor = len(CBase) -1
                CR , CB , CG = CBase[LEDColor]
                LED[0][0].set_color(RGBColor(CR , CB , CG))
                if LED[1][0] >= MaxOffset:
                    LED[1][0] = 1
                else:
                    LED[1][0] += 1

CustomRainbow()