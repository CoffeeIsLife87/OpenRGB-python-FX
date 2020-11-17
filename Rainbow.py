import openrgb , time , string , colorsys, sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

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
            Speed = sys.argv[(sys.argv.index(arg) + 1)]
        else:
            pass
    return(Color1, Color2, Speed, ReversedDevice, OnlySet)

def CreateCBase():
    Cbase = []
    CycleSpeed = 300
    hue_range = CycleSpeed
    for i in range(hue_range):
        color = colorsys.hsv_to_rgb(i / hue_range, 1.0, 1.0)

        # Split RGB values
        R = int(color[0] * 255)
        G = int(color[1] * 255)
        B = int(color[2] * 255)
        Cbase += [RGBColor(R,G,B)]
    return(Cbase)

def CustomRainbow(CBase, ZoneOffsets, MaxOffset): #Higher Offset = slower
    Color = len(CBase)/MaxOffset # MaxOffset changes now but for some numbers it is buggy but I am too lazy to figure out why so it defaults to 30 (which isn't buggy)
    while True: # Run infinitely
        for ZO in ZoneOffsets: # Grab a zone created earlier
            ZOType = ZO[0].type
            if ZOType == ZoneType.MATRIX:
                pass
            elif ZOType != ZoneType.MATRIX:
                ID = 0 # Switched to a counter based method since for some reason the .index method spat out broken numbers
                if ZO[3] == True:
                    for _ in ZO[0].colors: # enumerate through the color entries in the zone object
                        FinalColor = Color*ZO[1][ID] # get the color to put on the LED
                        if FinalColor >= len(CBase): # make sure that it isn't out of bounds
                            FinalColor = len(CBase) - 1
                        ZO[0].colors[ID] = CBase[int(FinalColor)] # Tell the zone to set that LED to the color
                        if ZO[1][ID] <= 1: # check to make sure that the offset isn't out of bounds
                            ZO[1][ID] = MaxOffset
                        else:
                            ZO[1][ID] -= 1 # make the offset go up one
                        ID += 1
                elif ZO[3] == False:
                    for _ in ZO[0].colors: # enumerate through the color entries in the zone object
                        FinalColor = Color*ZO[1][ID] # get the color to put on the LED
                        if FinalColor >= len(CBase): # make sure that it isn't out of bounds
                            FinalColor = len(CBase) - 1
                        ZO[0].colors[ID] = CBase[int(FinalColor)] # Tell the zone to set that LED to the color
                        if ZO[1][ID] >= MaxOffset: # check to make sure that the offset isn't out of bounds
                            ZO[1][ID] = 1
                        else:
                            ZO[1][ID] += 1 # make the offset go up one
                        ID += 1
            ZO[0].show() # paint all the LEDs set in the zone
        time.sleep(0.1) # sleep so the controller can cool down

if __name__ == "__main__":
    _, _, Speed, Reversed, Enabled = UserInput()

    if Speed != None:
        MaxOffset = Speed
    elif Speed == None:
        Speed = 30
    
    Enable = []
    if Enabled == None:
        Enable += [i for i in client.devices]
    elif Enabled != None:
        Enable = Enabled

    SetStatic(Enable)

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
    #print(PassTo)

    CustomRainbow(CreateCBase(),PassTo,Speed)
    