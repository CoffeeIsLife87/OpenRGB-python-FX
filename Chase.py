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
            if ' , ' in sys.argv[ReversedDevices]:
                ReversedDevice = []
                for i in sys.argv[ReversedDevices].split(' , '):
                    for D in client.devices:
                        if D.name.strip().casefold() == i.strip().casefold():
                            ReversedDevice += [D.name]
            else:
                for D in client.devices:
                    if D.name.strip().casefold() == sys.argv[ReversedDevices].strip().casefold():
                        ReversedDevice = [D.name]
        elif arg == '--only-set':
            AllowedDevices = (sys.argv.index(arg) + 1)
            if ' , ' in sys.argv[AllowedDevices]:
                for i in sys.argv[AllowedDevices].split(' , '):
                    OnlySet = []
                    for D in client.devices:
                        if D.name.strip().casefold() == i.strip().casefold():
                            OnlySet += [D.name]
            else:
                for D in client.devices:
                    if D.name.strip().casefold() == sys.argv[AllowedDevices].strip().casefold():
                        OnlySet = [D.name]
        else:
            pass
    return(Color1, Color2, ReversedDevice, OnlySet)

print(UserInput())

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

def InfiniteCycle(C1, C2, Enabled, reversed):
    ZoneOffsets = []
    for Device in Enabled:
        for zone in Device.zones:
            LEDAmmount = len(zone.leds) # the ammount of leds in a zone
            ZoneOffsets = ZoneOffsets + [[zone, [i for i in range(1, (LEDAmmount + 1)) ], LEDAmmount ]] #setup the zone and add an offset tracker
            
    while True:
        for ZO in ZoneOffsets:
            ID = 0
            Half = int(len(ZO[0].colors)/2)
            for _ in ZO[0].colors:
                if ZO[1][ID] >= Half:
                    ZO[0].colors[ID] = C1
                elif ZO[1][ID] < Half:
                    ZO[0].colors[ID] = C2
                if ZO[1][ID] == ZO[2]:
                    ZO[1][ID] = 1
                else:
                    ZO[1][ID] += 1
                ID += 1
            ZO[0].show()
        time.sleep(0.01)

if __name__ == '__main__':
    C1, C2, Reversed, Enabled = UserInput()
    if C1 == None:
        C1 = RGBColor(255,0,0)
    if C2 == None:
        C2 = RGBColor(0,0,255)
    if Enabled == None:
        Enable = []
        Enable += [i for i in client.devices]
    if Reversed == None:
        Reverse = None
    InfiniteCycle(C1,C2,Enable,Reversed)