import openrgb , time , string , colorsys, sys
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

def CustomRainbow(MaxOffset=30): #Higher Offset = slower

    def CreateColorBase(CycleSpeed=15):#you must be able to devide 255 by CycleSpeed or THIS WILL NOT WORK
        CBase = []
        R = 240
        G = B = 0
        while True:
            R += 3
            CBase = CBase + [(R,G,B)]
            if R == 255:
                while True:
                    G += CycleSpeed
                    CBase = CBase + [(R,G,B)]
                    if G == 255:
                        while True:
                            R -= CycleSpeed
                            CBase = CBase + [(R,G,B)]
                            if R == 0:
                                while True:
                                    B += CycleSpeed
                                    CBase = CBase + [(R,G,B)]
                                    if B == 255:
                                        while True:
                                            G -= CycleSpeed
                                            CBase = CBase + [(R,G,B)]
                                            if G == 0:
                                                while True:
                                                    R += CycleSpeed
                                                    CBase = CBase + [(R,G,B)]
                                                    if R == 255:
                                                        while True:
                                                            B -= CycleSpeed
                                                            CBase = CBase + [(R,G,B)]
                                                            if B == 0:
                                                                return CBase

    def GrabColorOrSpeedOrBoth(Enable=3):
        """Another function for easy copy and pasting\n
        CreateCbase has to be defined for this to work or you have to modify it\n
        You can also enable or disable certain parts (1 is only enable color, 2 is only speed, 3 is both enabled)"""
        if (Enable == 1) or (Enable == 3):
            if (len(sys.argv) == 4):
                #CB = CreateCBase(C=(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])))
                FastGoBRR = 15
                print('user defined color')
    
        if (Enable == 2) or (Enable == 3):
            if len(sys.argv) == 2:
                CB = CreateColorBase()
                FastGoBRR = int(sys.argv[1])
                #print('user defined speed')
        
        if (Enable == 3):
            if len(sys.argv) == 5:
                CB = CreateColorBase()
                FastGoBRR = int(sys.argv[1])
                #print('user defined both')
        
        else:
            CB = CreateColorBase()
            FastGoBRR = 15
            #print('nothing is user defined')
        return CB, FastGoBRR

    CBase, MaxOffset = GrabColorOrSpeedOrBoth(2)

    ZoneOffsets = []
    for Device in Dlist:
        for zone in Device.zones:
            LEDAmmount = len(zone.leds) # the ammount of leds in a zone
            ZoneOffsets = ZoneOffsets + [[zone, [i for i in range(1, (LEDAmmount + 1)) ], LEDAmmount ]] #setup the zone and add an offset tracker
    
    Color = len(CBase)/MaxOffset # MaxOffset changes now but for some numbers it is buggy but I am too lazy to figure out why so it defaults to 30 (which isn't buggy)
    while True: # Run infinitely
        for ZO in ZoneOffsets: # Grab a zone created earlier
            for color in ZO[0].colors: # enumerate through the color entries in the zone object
                ID = ZO[0].colors.index(color) # grab the current item index for use later (I figured this was more effective than grabbing it a lot later)
                FinalColor = Color*ZO[1][ID] # get the color to put on the LED
                if FinalColor >= len(CBase): # make sure that it isn't out of bounds
                    FinalColor = len(CBase) - 1
                CR, CG, CB = CBase[int(FinalColor)]# devide it for the RGBColor module (it is really picky)
                ZO[0].colors[ID] = RGBColor(CR, CG, CB) # Tell the zone to set that LED to the color
                if ZO[1][ID] >= MaxOffset: # check to make sure that the offset isn't out of bounds
                    ZO[1][ID] = 1
                else:
                    ZO[1][ID] += 1 # make the offset go up one
            ZO[0].show() # paint all the LEDs set in the zone
        time.sleep(0.1) # sleep so the controller can cool down

CustomRainbow() # not sure why I wrote all this as a function '_'
# I suppose if I every merge it all into one file then it might help