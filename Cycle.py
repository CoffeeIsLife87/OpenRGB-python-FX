import openrgb , time , string , colorsys, sys
from openrgb.utils import RGBColor , ModeData

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

def SetStatic(DList):
    for Device in DList:
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

def CustomSpectrumCycle(CycleSpeed=1000):
    while True:
        #credit to @James Potkukelkka on discord for MOST of the code
        hue_range = CycleSpeed # Smaller = faster
        iteration_delay = 0.01 # 10ms
        for i in range(hue_range):
            color = colorsys.hsv_to_rgb(i / hue_range, 1.0, 1.0)

            # Split RGB values
            red = color[0] * 255
            green = color[1] * 255
            blue = color[2] * 255

            for Device in DList:
                Device.set_color(RGBColor(int(red),int(green),int(blue)))
                time.sleep(iteration_delay)

if __name__ == '__main__':
    _,_,_,_,Enabled = UserInput()
    DList = []
    if Enabled == None:
        DList += [i for i in client.devices]
    elif Enabled != None:
        DList += [i for i in Enabled]
    SetStatic(DList)
    CustomSpectrumCycle()