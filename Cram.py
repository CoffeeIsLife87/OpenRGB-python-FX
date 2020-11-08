import openrgb , time , sys , random
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

def UserInput():
    """It will always return 5 things;\n
    Color1, Color2, Speed, Devices for reversal, Devices that are enables"""
    Color1 = Color2 = Speed = ReversedDevice = OnlySet = None
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
            ReversedDevices = (sys.argv.index(arg) + 1) # Will point to where the device(s) that need to be reversed are
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
            AllowedDevices = (sys.argv.index(arg) + 1) # Will point to where the device(s) that are allowed are
            OnlySet = []
            if ' , ' in sys.argv[AllowedDevices]:
                for i in sys.argv[AllowedDevices].split(' , '):
                    for D in client.devices:
                        if D.name.strip().casefold() == i.strip().casefold():
                            OnlySet += [D]
            else:
                for D in client.devices:
                    if D.name.strip().casefold() == sys.argv[AllowedDevices].strip().casefold():
                        OnlySet += [D]
        elif arg == '--speed':
            Speed = int(sys.argv[(sys.argv.index(arg) + 1)])
        else:
            pass
    return(Color1, Color2, Speed, ReversedDevice, OnlySet)

def RandomColor(MinVal=200):
    """
    MinVal will be the smallest number you are ok with
    The higher the number, the brighter the resulting color will be
    """
    while True:
        CR = random.randint(0,255)
        CG = random.randint(0,255)
        CB = random.randint(0,255)
        if (CR + CG + CB) >= MinVal:
            return CR, CG, CB

if __name__ == '__main__':
    C1,_,_,_,Enabled = UserInput()
    
    Dlist = []

    if Enabled == None:
        Dlist += [i for i in client.devices]
    if Enabled != None:
        Dlist += [i for i in Enabled]

    Check = 0
    for i in Dlist:
        Bigger = len(i.leds)
        if Check < Bigger:
            Check = Bigger
    print(Check)

    if C1 == None:
        Color = 0
    elif C1 != None:
        Color = C1

    while True:
        Num = 0
        if Color == 0:
            R, G, B = RandomColor()
            NewColor = RGBColor(R,G,B)
        else:
            NewColor = Color
        while Num <= Check:
            for Device in Dlist:
                try:
                    Device.leds[Num].set_color(NewColor)
                except:
                    pass
            Num += 1
            time.sleep(0.1)
        time.sleep(1)
        for Device in Dlist:
            Device.set_color(RGBColor(0,0,0))
            time.sleep(0.01)
        time.sleep(0.5)
