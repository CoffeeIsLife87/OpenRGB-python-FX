import openrgb, time, sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

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

def TempAware(DL):
    import clr # the pythonnet module. You might need to install it 'pip install pythonnet'
    clr.AddReference('TempAware\\OpenHardwareMonitorLib.dll') #enter your dll path 
    from OpenHardwareMonitor.Hardware import Computer
    tempature =0
    colorplusdown = 0
    c = Computer()
    c.CPUEnabled = True # get the Info about CPU
    c.GPUEnabled = True # get the Info about GPU
    c.Open()
    for DName in range(0, len(c.Hardware)):
        if ("GPU" in str(c.Hardware[DName])) or ("gpu" in str(c.Hardware[DName])):
            while True:
                for Sen in range(0 , (len(c.Hardware[DName].Sensors))):
                    if "temperature" in str(c.Hardware[1].Sensors[Sen].Identifier):
                        tempature = (c.Hardware[1].Sensors[Sen].get_Value())
                        print(tempature)
                        c.Hardware[1].Update()
                        if 19 > tempature:
                            for Device in DL:
                                colorplusdown = (tempature) * 255/19
                                Device.set_color(RGBColor(int(0), int(0+colorplusdown), int(255)))
                            time.sleep(1)  
                        elif 38 > tempature >= 19:
                            for Device in DL:
                                colorplusdown = (tempature-19) * 255/19
                                Device.set_color(RGBColor(int(0), int(255), int(255-colorplusdown)))
                            time.sleep(1)
                        elif 57 > tempature >= 38:
                            for Device in DL:
                                colorplusdown = (tempature-38) * 255/19
                                Device.set_color(RGBColor(int(0+colorplusdown), int(255), int(0)))
                            time.sleep(1)
                        elif 76 >= tempature >= 57:
                            for Device in DL:
                                colorplusdown = (tempature-57) * 255/10
                                Device.set_color(RGBColor(int(255), int(255-colorplusdown), int(0)))
                            time.sleep(1)

if __name__ == "__main__":
    _ , _ , _ , _ , DeviceList = UserInput()
    if DeviceList == None:
        NewDeviceList = []
        NewDeviceList += [i for i in client.devices]
    SetStatic(NewDeviceList)
    TempAware(NewDeviceList)