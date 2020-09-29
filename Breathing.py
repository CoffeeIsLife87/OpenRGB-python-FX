import openrgb , time , string , colorsys , sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

def CreateCBase(C = (0,25,255)):
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

CB = CreateCBase()

def FBounce(ColorWall):
    for color in ColorWall:
        for Device in Dlist:
            Device.set_color(RGBColor(color[0], color[1], color[2]))
            time.sleep(0.0001)
    time.sleep(3)

def BBounce(ColorWall):
    for color in reversed(ColorWall):
        for Device in Dlist:
            Device.set_color(RGBColor(color[0], color[1], color[2]))
            time.sleep(0.0001)
    time.sleep(1)

while True:
    FBounce(CB)
    BBounce(CB)
