import openrgb , time , string , colorsys , sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

def SetStatic():
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

Red = RGBColor(255,0,0)
Black = RGBColor(0,0,0)

def MakeSurfaceList():
    SurfaceList = []
    for D in Dlist:
        for Z in D.zones:
            if Z.type == ZoneType.LINEAR:
                SurfaceList = SurfaceList + [Z]
    return SurfaceList 

Slist = MakeSurfaceList()

def AddOffsets(SL):
    LedOffsetMap = []
    for S in SL:
        ZoneMap = []
        LEDOffset = len(S.leds)
        for led in S.leds:
            #LEDOffset -= 1
            ZoneMap = ZoneMap + [[led , LEDOffset]]
            LEDOffset -= 1
        LedOffsetMap = LedOffsetMap + [ZoneMap]
    return LedOffsetMap

LedOffsetMap = (AddOffsets(Slist))

def MakeDRain(LOffsetMap):
    #NumOfDrops = len(Zone.leds)
    #print(LedOffsetMap)
    while True:
        for Check in LOffsetMap[0]:
            if (Check[1] == 1) or (Check[1] == 2):
                Check[0].set_color(Red)
                if Check[1] == 1:
                    Check[1] = 10
                else:
                    Check[1] -= 1
                print(Check[1])
            else:
                Check[0].set_color(Black)
                Check[1] -= 1
            #print(Check[1])
            time.sleep(0.1)
        #return
    #Zone.leds[0].set_color(Red)
    #for LED in Zone.leds:

MakeDRain(LedOffsetMap)