import openrgb , time , string , colorsys , sys , threading , random
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

#print(random.randint(1,2))

#exit()
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

#Color = RGBColor(0,127,255)
Red = RGBColor(255,0,0)
Black = RGBColor(0,0,0)

def MakeSurfaceList():
    SurfaceList = []
    for D in Dlist:
        for Z in D.zones:
            if Z.type == ZoneType.LINEAR:
                SurfaceList = SurfaceList + [Z]
    return SurfaceList # Rain is really hard to do on single or matrix maps so I will stick to linear for now. I may add matrix support for keyboards but that will be for the future

def AddOffsets(SL):
    LedOffsetMap = []
    for S in SL:
        ZoneMap = []
        LEDOffset = len(S.leds)
        for led in S.leds:
            ZoneMap = ZoneMap + [[led , LEDOffset]]
            LEDOffset -= 1
        LedOffsetMap = LedOffsetMap + [ZoneMap]
    return LedOffsetMap

def MakeDRain(PreserveMap):
    LOffsetMap = PreserveMap
    try:
        while True:
            for Sub in LOffsetMap:
                for Check in Sub:
                    if (Check[1] == 1) or (Check[1] == 2):
                        Check[0].set_color(Red)
                        if Check[1] == -1:
                            pass
                        else:
                            Check[1] -= 1
                    else:
                        Check[0].set_color(Black)
                        if Check[1] == -1:
                            pass
                        else:
                            Check[1] -= 1
                    time.sleep(0.01)
            if LedOffsetMap[0][0][1] == -1:
                break
    except:
        while True:
            for Check in LOffsetMap:
                if (Check[1] == 1) or (Check[1] == 2):
                    Check[0].set_color(Red)
                    if Check[1] == -1:
                        pass
                    else:
                        Check[1] -= 1
                else:
                    Check[0].set_color(Black)
                    if Check[1] == -1:
                        pass
                    else:
                        Check[1] -= 1
                time.sleep(0.01)
            if LedOffsetMap[0][0][1] == -1:
                break
    return

def EnsureRandom(LOM):
    NoDupes = []
    Num = 1
    for i in LOM:
        T = threading.Thread(group=None,name=Num,target=MakeDRain(i),daemon=True)
        NoDupes = NoDupes + [[T,Num]]
        Num += 1
    while True:
        time.sleep(1)
        print("loop")
        for I in NoDupes:
            if random.randint(1,2) == 1:
                pass

Slist = MakeSurfaceList()
LedOffsetMap = (AddOffsets(Slist))
EnsureRandom(LedOffsetMap)
#MakeDRain(LedOffsetMap)