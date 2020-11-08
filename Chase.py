import openrgb, time, sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

def UserInput():
    Color1 = Color2 = ReversedDevice = OnlySet = None
    for arg in sys.argv:
        if arg == '--C1':
            Pos = sys.argv.index(arg) + 1
            R, G, B = sys.argv[Pos:(Pos + 3)]
            Color1 = RGBColor(int(R),int(G),int(B))
        elif arg == '--C2':
            Pos = sys.argv.index(arg) + 1
            R, G, B = sys.argv[Pos:(Pos + 3)]
            Color2 = RGBColor(int(R),int(G),int(B))
        elif arg == '--reversed':
            ReversedDevices = (sys.argv.index(arg) + 1)
            ReversedDevice = []
            if ' , ' in sys.argv[ReversedDevices]:
                for i in sys.argv[ReversedDevices].split(' , '):
                    for D in client.devices:
                        if D.name.strip().casefold() == i.strip().casefold():
                            ReversedDevice += [D]
            else:
                for D in client.devices:
                    if D.name.strip().casefold() == sys.argv[ReversedDevices].strip().casefold():
                        ReversedDevice += [D]
        elif arg == '--only-set':
            OnlySet = []
            AllowedDevices = (sys.argv.index(arg) + 1)
            if ' , ' in sys.argv[AllowedDevices]:
                for i in sys.argv[AllowedDevices].split(' , '):
                    for D in client.devices:
                        if D.name.strip().casefold() == i.strip().casefold():
                            OnlySet += [D]
            else:
                for D in client.devices:
                    if D.name.strip().casefold() == sys.argv[AllowedDevices].strip().casefold():
                        OnlySet += [D]
        else:
            pass
    return(Color1, Color2, ReversedDevice, OnlySet)

def SetStatic(Dlist):
    """A quick function I use to make sure that everything is in direct or static mode"""
    for Device in Dlist:
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

def InfiniteCycle(C1, C2, ZoneOffsets):
    RunThrough = 0
    while True:
        for ZO in ZoneOffsets:
            ZOType = ZO[0].type
            if ZOType == ZoneType.SINGLE:
                RunThrough += 1
                if (RunThrough%3) == 0:
                    if ZO[0].colors[0] == C1:
                        ZO[0].colors[0] = (C2)
                    elif ZO[0].colors[0] == C2:
                        ZO[0].colors[0] = (C1)
                    elif (ZO[0].colors[0] != C1) & (ZO[0].colors[0] != C2):
                        ZO[0].colors[0] = (C2)
                    ZO[0].show()
            elif ZOType == ZoneType.LINEAR:
                if ZO[3] == True: # True is reversed, False is regular
                    ID = 0
                    Half = int(len(ZO[0].colors)/2)
                    for _ in ZO[0].colors:
                        if ZO[1][ID] > Half:
                            ZO[0].colors[ID] = C1
                        elif ZO[1][ID] <= Half:
                            ZO[0].colors[ID] = C2
                        if ZO[1][ID] >= ZO[2]:
                            ZO[1][ID] = 1
                        else:
                            ZO[1][ID] += 1
                        ID += 1
                    ZO[0].show()
                elif ZO[3] == False:
                    ID = 0
                    Half = int(len(ZO[0].colors)/2)
                    for _ in ZO[0].colors:
                        if ZO[1][ID] >= Half:
                            ZO[0].colors[ID] = C1
                        elif ZO[1][ID] < Half:
                            ZO[0].colors[ID] = C2
                        if ZO[1][ID] <= 0:
                            ZO[1][ID] = ZO[2]
                        else:
                            ZO[1][ID] -= 1
                        ID += 1
                    ZO[0].show()
            elif ZOType == ZoneType.MATRIX:
                pass
                #print('matrix support not done yet')
        time.sleep(0.1)

if __name__ == '__main__':
    C1, C2, Reversed, Enabled = UserInput()
    print(C1, C2, Reversed, Enabled)
    if C1 == None:
        C1 = RGBColor(255,0,0)
    if C2 == None:
        C2 = RGBColor(0,0,255)
    Enable = []
    if Enabled == None:
        Enable += [i for i in client.devices]
    elif Enabled != None:
        Enable = Enabled

    PassTo = []
    for Device in Enable:
        if Reversed != None:
            for R in Reversed:
                if R == Device:
                    ReverseBool = True
                    continue
                else:
                    ReverseBool = False
        else:
            ReverseBool = False
        for zone in Device.zones:
            LEDAmmount = len(zone.leds) # the ammount of leds in a zone
            PassTo += [[zone, [i for i in range(1, (LEDAmmount + 1)) ], LEDAmmount, ReverseBool]]
    
    SetStatic(Enable)
    InfiniteCycle(C1, C2, PassTo)