import openrgb , time , string , colorsys , sys
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
    RGBColor, RGBColor, int, list, list\n
    Color1, Color2, Speed, Devices for reversal, Devices that are enables"""
    Color1 = Color2 = Speed = ReversedDevice = OnlySet = None
    for arg in sys.argv:
        if arg == '--C1':
            Pos = sys.argv.index(arg) + 1
            R, G, B = sys.argv[Pos:(Pos + 3)]
            Color1 = [int(R),int(G),int(B)]
        elif arg == '--C2':
            Pos = sys.argv.index(arg) + 1
            R, G, B = sys.argv[Pos:(Pos + 3)]
            Color2 = [int(R),int(G),int(B)]
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

def MakeCBase(StartingColor=None,EndingColor=None):
    def hex_to_RGB(hex):
        ''' "#FFFFFF" -> [255,255,255] '''
        # Pass 16 to the integer function for change of base
        return [int(hex[i:i+2], 16) for i in range(1,6,2)]

    def RGB_to_hex(RGB):
        ''' [255,255,255] -> "#FFFFFF" '''
        # Components need to be integers for hex to make sense
        RGB = [int(x) for x in RGB]
        return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                  "{0:x}".format(v) for v in RGB])

    def color_dict(gradient):
        ''' Takes in a list of RGB sub-lists and returns dictionary of
        colors in RGB and hex form for use in a graphing function
        defined later on '''
        return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
            "r":[RGB[0] for RGB in gradient],
            "g":[RGB[1] for RGB in gradient],
            "b":[RGB[2] for RGB in gradient]}

    def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
        ''' returns a gradient list of (n) colors between
        two hex colors. start_hex and finish_hex
        should be the full six-digit color string,
        inlcuding the number sign ("#FFFFFF") '''
        # Starting and ending colors in RGB form
        s = hex_to_RGB(start_hex)
        f = hex_to_RGB(finish_hex)
        # Initilize a list of the output colors with the starting color
        RGB_list = [s]
        # Calcuate a color at each evenly spaced value of t from 1 to n
        for t in range(1, n):
            # Interpolate RGB vector for color at the current value of t
            curr_vector = [
              int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
              for j in range(3)
            ]
            # Add it to our list of output colors
            RGB_list.append(curr_vector)

        return color_dict(RGB_list)

    def polylinear_gradient(colors, n):
        ''' returns a list of colors forming linear gradients between
        all sequential pairs of colors. "n" specifies the total
        number of desired output colors '''
        # The number of colors per individual linear gradient
        n_out = int(float(n) / (len(colors) - 1))
        # returns dictionary defined by color_dict()
        gradient_dict = linear_gradient(colors[0], colors[1], n_out)

        if len(colors) > 1:
            for col in range(1, len(colors) - 1):
                next = linear_gradient(colors[col], colors[col+1], n_out)
                #for k in ("hex", "r", "g", "b"):
                for k in ("r", "g", "b"):
                    # Exclude first point to avoid duplicates
                    gradient_dict[k] += next[k][1:]

        return gradient_dict

    Grad = polylinear_gradient((RGB_to_hex(StartingColor),RGB_to_hex(EndingColor),RGB_to_hex(StartingColor)),90)

    RList , GList , BList = Grad['r'], Grad['g'], Grad['b']

    def FinishCbase(R , G , B):
        Cbase = []
        ListPos = 0
        while ListPos < len(R):
            C = RGBColor(R[ListPos],G[ListPos],B[ListPos])
            Cbase += [C]
            ListPos += 1
        return Cbase

    ColorBase = FinishCbase(RList,GList,BList)

    return ColorBase

def GradCycle(CBase, ZoneOffsets, MaxOffset):
    Color = len(CBase)/MaxOffset # MaxOffset changes now but for some numbers it is buggy but I am too lazy to figure out why so it defaults to 30 (which isn't buggy)
    while True: # Run infinitely
        for ZO in ZoneOffsets: # Grab a zone created earlier
            ZOType = ZO[0].type
            if ZOType == ZoneType.MATRIX:
                pass
            elif ZOType != ZoneType.MATRIX:
                ID = 0
                if ZO[3] == True:
                    for _ in ZO[0].colors: # enumerate through the color entries in the zone object
                        FinalColor = int(Color*ZO[1][ID]) # get the color to put on the LED
                        if FinalColor >= len(CBase): # make sure that it isn't out of bounds
                            FinalColor = int(len(CBase) - 1)
                        ZO[0].colors[ID] = CBase[FinalColor] # Tell the zone to set that LED to the color
                        if ZO[1][ID] <= 1: # check to make sure that the offset isn't out of bounds
                            ZO[1][ID] = MaxOffset
                        else:
                            ZO[1][ID] -= 1 # make the offset go up one
                        ID += 1
                elif ZO[3] == False:
                    for _ in ZO[0].colors: # enumerate through the color entries in the zone object
                        FinalColor = int(Color*ZO[1][ID]) # get the color to put on the LED
                        if FinalColor >= len(CBase): # make sure that it isn't out of bounds
                            FinalColor = int(len(CBase) - 1)
                        ZO[0].colors[ID] = CBase[FinalColor] # Tell the zone to set that LED to the color
                        if ZO[1][ID] >= MaxOffset: # check to make sure that the offset isn't out of bounds
                            ZO[1][ID] = 1
                        else:
                            ZO[1][ID] = ZO[1][ID] + 1 # make the offset go up one
                        ID += 1
            ZO[0].show() # paint all the LEDs set in the zone
            #time.sleep(5)
        time.sleep(0.1) # sleep so the controller can cool down

if __name__ == '__main__':
    
    C1 , C2 , Speed, Reversed, Enabled = UserInput()
    if C1 == None:
        C1 = [0,255,255]
    if C2 == None:
        C2 = [120,0,255]
 
    Cbase = MakeCBase(C1,C2)

    if Speed == None:
        Speed = 15

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

    GradCycle(Cbase, PassTo, Speed)