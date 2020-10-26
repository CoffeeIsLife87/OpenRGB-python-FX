import openrgb, time, sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

C1 = RGBColor(255, 0, 0)
C2 = RGBColor(0, 0, 255)

def SetStatic():
    """A quick function I use to make sure that everything is in direct or static mode"""
    for Device in client.devices:
        time.sleep(0.1)
        try:
            Device.set_mode('direct')
            print('Set %s successfully'%Device.name)
        except:
            try:
                Device.set_mode('static')
                print('error setting %s\nfalling back to static'%Device.name)
            except:
                print("Critical error! couldn't set %s to static or direct"%Device.name)
SetStatic()

ZoneOffsets = []
for Device in Dlist:
    for zone in Device.zones:
        LEDAmmount = len(zone.leds) # the ammount of leds in a zone
        ZoneOffsets = ZoneOffsets + [[zone, [i for i in range(1, (LEDAmmount + 1)) ], LEDAmmount ]] #setup the zone and add an offset tracker

def InfiniteCycle():
    while True:
        for ZO in ZoneOffsets:
            Run = 0
            Half = int(len(ZO[0].colors)/2)
            for _ in ZO[0].colors:
                if ZO[1][Run] >= Half:
                    ZO[0].colors[Run] = C1
                elif ZO[1][Run] < Half:
                    ZO[0].colors[Run] = C2

                if ZO[1][Run] == ZO[2]:
                    ZO[1][Run] = 1
                else:
                    ZO[1][Run] += 1
                Run += 1
            ZO[0].show()

InfiniteCycle()