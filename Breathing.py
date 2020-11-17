import openrgb , time , string , colorsys , sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

def SetStatic(DList):
    """A quick function I use to make sure that everything is in direct or static mode"""
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

def CreateCBase(C = (255,255,255)):
    """Creates a data base of 255 colors to index for use later\n
    So you can grab an RGB color with ``Cbase[num]`` and have a color code\n
    I am not sure if this makes it faster or not but I would assume since it doesn't have to do the math to find out what color it should be
    """
    RunThrough = 0 # determines the amount of passes made
    DevideBase = 0 # the highest value of C (RGB color code)
    BaseC = C #to preserve C for use later (mostly for devision)
    CBase = [] # an empty list to drop the color base into
    for i in C:
        if i > DevideBase:
            DevideBase = i # Redefines DevideBase to be the actually highest instead of 0
    while (C[0] + C[1] + C[2]) > 0: # create a color base for the effect for use later until all three added is == 0 (fade to black)
        AddC = []
        for i in C:
            if (BaseC[C.index(i)] != 0) & (int(BaseC[C.index(i)]) != int(DevideBase)): # the first portion ensure that it isn't trying to devide by 0. the second is to ensure that it doesn't try to devide a number by itself and waste time
                if RunThrough % int(DevideBase / BaseC[C.index(i)]) == 0: # I forgot how this works but it does
                    i -= 1
            else:
                if i > 0: # only subtract if it is greater than 0 (to avoid the SDK yelling at me)
                    i -= 1 # subtract
            AddC += [i] # add all the numbers together again to get the color code
        RunThrough += 1 # increase the pass amount
        #print(AddC) # print the color code for debugging (will be commented for release)
        C = AddC # This is neccisary for ensure it doesn't get stuck in a loop due to it comparing a static value in the While loop
        CBase += [C]
    return CBase

def UserInput():
    """It will always return 5 things;\n
    Color1, Color2, Speed, Devices for reversal, Devices that are enables"""
    Color1 = Color2 = Speed = ReversedDevice = OnlySet = None
    for arg in sys.argv:
        if arg == '--C1':
            Pos = sys.argv.index(arg) + 1
            R, G, B = sys.argv[Pos:(Pos + 3)]
            Color1 = RGBColor(R,G,B)
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

def FBounce(ColorWall,Speed): # makes the lights get brighter
    for color in ColorWall:
        if (ColorWall.index(color)%Speed == 0) or (ColorWall.index(color) == 254):
            if (ColorWall.index(color) == 254):
                for Device in DList:
                    Device.set_color(RGBColor(color[0], color[1], color[2]))
                    time.sleep(0.1)
            else:
                for Device in DList:
                    Device.set_color(RGBColor(color[0], color[1], color[2]))
                    time.sleep(0.01)
    time.sleep(2)

def BBounce(ColorWall,Speed): # makes the lights get darker
    for color in reversed(ColorWall):
        if (ColorWall.index(color)%Speed == 0):
            for Device in DList:
                Device.set_color(RGBColor(color[0], color[1], color[2]))
                time.sleep(0.01)

if __name__ == '__main__':
    C1,_,Speed,_,Enabled = UserInput()
    if C1 != None:
        CBase = CreateCBase(C1)
    elif C1 == None:
        CBase = CreateCBase()
    if Speed == None:
        Speed = 15
    DList = []
    if Enabled == None:
        DList += [i for i in client.devices]
    elif Enabled != None:
        DList += [i for i in Enabled] 
    while True:
        FBounce(CBase,Speed)
        BBounce(CBase,Speed)
