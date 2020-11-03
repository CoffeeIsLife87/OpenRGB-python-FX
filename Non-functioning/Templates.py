#This is a file containing only templates for certain functions

#---------------------Color Base generators----------------------------------
def CreateCBaseFTB(C = (255,255,255)):
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
            AddC = AddC + [i] # add all the numbers together again to get the color code
        RunThrough += 1 # increase the pass amount
        #print(AddC) # print the color code for debugging (will be commented for release)
        C = AddC # This is neccisary for ensure it doesn't get stuck in a loop due to it comparing a static value in the While loop
        CBase = CBase + [C]
    return CBase
# ^ This one is Fade to black (you can reverse from black to original using reverse(Cbase) )

def CreateCBaseRainbow(CycleSpeed=15):
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
# ^ This one is for creating a rainbow wave (red -> orange -> yellow -> green -> blue -> purple -> red)

#---------------------User input---------------------------------------------
def GrabColorOrSpeedOrBoth(Enable=3):
    """Another function for easy copy and pasting\n
    CreateCbase has to be defined for this to work or you have to modify it\n
    You can also enable or disable certain parts (1 is only enable color, 2 is only speed, 3 is both enabled)"""
    if (Enable == 1) or (Enable == 3):
        if (len(sys.argv) == 4):
            CB = CreateCBase(C=(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])))
            FastGoBRR = 15
            print('user defined color')

    if (Enable == 2) or (Enable == 3):
        if len(sys.argv) == 2:
            CB = CreateCBase()
            FastGoBRR = int(sys.argv[1])
            #print('user defined speed')
            if len(CB)%FastGoBRR != 0:
                print('255 is not devisable by %f (Defaulting to 15)\nPlease try to pick a number that is'%FastGoBRR)
                FastGoBRR = 15
    
    if (Enable == 3):
        if len(sys.argv) == 5:
            CB = CreateCBase(C=(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])))
            FastGoBRR = int(sys.argv[1])
            #print('user defined both')
    
    else:
        CB = CreateCBase()
        FastGoBRR = 15
        #print('nothing is user defined')
    return CB, FastGoBRR

def CheckForReversed():
    """Checks for Reversed devices and reverses the ones tagged"""
    if any('--reversed' == i for i in sys.argv): #check if there is a reverse flag
        for i in sys.argv: # will run through all of the user input and check for the --reversed flag
            if i == '--reversed':
                ReversedDevices = (sys.argv.index(i) + 1) # Will point to where the device(s) that need to be reversed are

        #Now that we know that there is a device(s) that needs to be reversed we can begin to parse which ones
        #The syntax will be "Device name with spaces,Other device name" (the comma is necissary since idk when 1 device end and another begins without it)
        if ' , ' in sys.argv[ReversedDevices]:
            for i in sys.argv[ReversedDevices].split(' , '):
                for D in client.devices:
                    if D.name.strip().casefold() == i.strip().casefold():
                        print(D.name)
        else:
            for D in client.devices:
                if D.name.strip().casefold() == sys.argv[ReversedDevices].strip().casefold():
                    print(D.name)

#---------------------Set to Static------------------------------------------
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
# Some notes on this one ^
# time is a module that you need to import to use this
# Client is what I name a variable (client = openrgb.OpenRGBClient())

#-------------------Random color generator-----------------------------------
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
# You need to have "random" imported for this one