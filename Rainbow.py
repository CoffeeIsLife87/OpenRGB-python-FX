import openrgb , time , string , colorsys
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
    CB = CreateColorBase()

    CBase = CB

    def wait(): # just usefull to have
        time.sleep(0.01) # does anyone know if calling functions like this adds more time?
    
    ZoneOffsets = []
    for Device in Dlist:
        for zone in Device.zones:
            LEDAmmount = len(zone.leds) # the ammount of leds in a zone
            ZoneOffsets = ZoneOffsets + [[zone, [i for i in range(1, (LEDAmmount + 1)) ], LEDAmmount ]] #setup the zone and add an offset tracker
    
    Color = len(CBase)/MaxOffset # for some reason I put that in the while loop even tho MaxOffset never changes smh
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
        wait() # sleep so the controller can cool down

CustomRainbow() # not sure why I wrote all this as a function '_'
# I suppose if I every merge it all into one file then it might help