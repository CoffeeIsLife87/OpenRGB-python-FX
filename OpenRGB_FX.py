import threading , openrgb , time , string , multiprocessing , colorsys
from openrgb.utils import DeviceType , RGBColor , ModeData
from tkinter import colorchooser
import tkinter as tk
import numpy as np

client = openrgb.OpenRGBClient()

Dlist = client.devices

def Apply(ModeVar,CurrentDevice,C):
    _ , DeviceID = CurrentDevice.get().split(' (')
    DeviceID , _ = DeviceID.split(')')
    print(DeviceID)
    #Mode = ModeVar.get()
    #SetSpecific(Mode,DeviceID,Color=C)

def SetDeviceColors(R , G , B):#device, R , G , B):
    for i in Dlist:
        i.set_color(RGBColor(R,G,B))
        time.sleep(0.0003)

def wait():
    time.sleep(0.003)

def DebugRGB(R , G , B):# for printing the values that are being set
    Debug = 0
    if Debug == 1:
        print(R , G , B)
    else:
        return

def SetStatic():
    for Device in client.devices:
        print(Device.name,Device.id)
        wait()
        try:
            try:
                Device.set_mode('static')
            except:
                Device.set_mode('direct')
        except:
            print('Unable to set %s'%Device.name)

def CustomSpectrumCycle(CycleSpeed=3):#
    SetStatic()
    while True:
        #credit to @James Potkukelkka on discord for some of the code
        hue_range = 1000 # Smaller = faster
        iteration_delay = 0.01 # 10ms
        for i in range(hue_range):
            color = colorsys.hsv_to_rgb(i / hue_range, 1.0, 1.0)

            # Split RGB values
            red = color[0] * 255
            green = color[1] * 255
            blue = color[2] * 255

            for Device in Dlist:
                Device.set_color(RGBColor(int(red),int(green),int(blue)))
                time.sleep(iteration_delay)

def CustomRainbow(speed=1,MaxOffset=30): #Higher = slower
    for Device in Dlist:
        time.sleep(0.3)
        try:
            Device.set_mode('static')
        except:
            Device.set_mode('direct')
        finally:
            print('error setting %s'%Device.name)
            
    Offset = 1
    def P1(CycleSpeed=15):#you must be able to devide 255 by CycleSpeed or THIS WILL NOT WORK
        CBase = []
        R = G = B = 0
        while 1 == 1:
            R += CycleSpeed
            CBase = CBase + [(R,G,B)]
            if R == 255:
                while 1 == 1:
                    G += CycleSpeed
                    CBase = CBase + [(R,G,B)]
                    if G == 255:
                        while 1 == 1:
                            R -= CycleSpeed
                            CBase = CBase + [(R,G,B)]
                            if R == 0:
                                while 1 == 1:
                                    B += CycleSpeed
                                    CBase = CBase + [(R,G,B)]
                                    if B == 255:
                                        while 1 == 1:
                                            G -= CycleSpeed
                                            CBase = CBase + [(R,G,B)]
                                            if G == 0:
                                                while 1 == 1:
                                                    R += CycleSpeed
                                                    CBase = CBase + [(R,G,B)]
                                                    if R == 255:
                                                        while 1 == 1:
                                                            B -= CycleSpeed
                                                            CBase = CBase + [(R,G,B)]
                                                            #print(CBase)
                                                            if B == 0:
                                                                return CBase
    CB = P1()

    CBase = CB

    def wait():
        time.sleep(float('0.000%d'%speed))
    
    Zones = []
    num = 0

    for device in Dlist:
        for zone in device.zones:
            Zones = Zones + [[zone]]
            Offset = 1
            for led in zone.leds:
                Zones[num] = Zones[num] + [[[led],[Offset]]]
                Offset += 1
            num += 1
    
    while True:
        wait()
        for Z in Zones:
            #CheckVal = len(Z) -1
            for LED in Z[1:-1]:
                Color = len(CBase)/MaxOffset
                LEDColor = (int(Color)*LED[1][0])
                if LEDColor >= len(CBase):
                    LEDColor = len(CBase) -1
                CR , CB , CG = CBase[LEDColor]
                LED[0][0].set_color(RGBColor(CR , CB , CG))
                if LED[1][0] >= MaxOffset:
                    LED[1][0] = 1
                else:
                    LED[1][0] += 1

ModeList = [[]]
check = 0
RamNum = 0
def FormGUI():

    OpenRGB_FX = tk.Tk(screenName='OpenRGB FX',baseName='OpenRGB FX')
    OpenRGB_FX.minsize(600,400)
    OpenRGB_FX.title('OpenRGB FX')

    #------Device Frame---------
    #DLocations = tk.LabelFrame(None,width=300,height=300,bg='#3c423d')
    #RamZone = tk.Frame(master=DLocations,width=80,height=180)
    #DimmOne = tk.Frame(master=RamZone,width=20,height=180,padx=3)
    #DimmTwo = tk.Frame(master=RamZone,width=20,height=180,padx=3)
    #DimmThree = tk.Frame(master=RamZone,width=20,height=180,padx=3)
    #DimmFour = tk.Frame(master=RamZone,width=20,height=180,padx=3)

    #DimmOne.pack(side='left')
    #DimmTwo.pack(side='left')
    #DimmThree.pack(side='left')
    #DimmFour.pack(side='left')
    #RamZone.pack()
    #DLocations.pack(anchor='ne')
    
    #------Mode Frame---------
    SpecificDeviceFrame = tk.Frame(None)

    CurrentDevice = tk.StringVar(SpecificDeviceFrame)

    for Device in Dlist:
        D = "%s (%s) "%(Device.name , Device.id)
        try:
            DeviceList = DeviceList + [D]
        except:
            DeviceList = [D]

    DSubFrame = tk.Frame(SpecificDeviceFrame)

    ModeVar = tk.Variable(SpecificDeviceFrame)
    global check
    if check == 0:
        ModeMenu = tk.OptionMenu(DSubFrame,ModeVar,*ModeList)
        check += 1

    def ListEventHandler(event):
        DeviceName , _ = CurrentDevice.get().split(' (')
        for i in Dlist:
            if i.name == DeviceName:
                Mlist = []
                for mode in i.modes:
                    Mlist = Mlist + [mode.name]
                NewModeList = (Mlist)
                break

        def Refresh():
            ModeVar.set('')
            ModeMenu['menu'].delete(0,'end')

            if str(type(NewModeList)) != "<class 'NoneType'>":
                for Mode in NewModeList:
                    ModeMenu['menu'].add_command(label=Mode, command=tk._setit(ModeVar, Mode))
        Refresh()
    
    #------RGB controller presets---------
    ModeMenu = tk.OptionMenu(DSubFrame,ModeVar,*ModeList)
    ModeMenu.pack(side='left')
    
    def GetColor():
        global RGBValue
        Color = colorchooser.askcolor
        RGBValue = Color()

    ColorButton = tk.Button(DSubFrame,text='Pick Color',command=GetColor)
    ColorButton.pack(side='left')

    ApplyMode = tk.Button(DSubFrame,text='Apply',command=lambda: Apply(ModeVar,CurrentDevice,RGBValue))

    ApplyMode.pack(side='right')
    DSubFrame.pack(side='bottom')


    DeviceMenu = tk.OptionMenu(SpecificDeviceFrame,CurrentDevice,*DeviceList,command=(ListEventHandler))
    DeviceMenu.pack(side='top')

    SpecificDeviceFrame.pack(side='left')

    SystemWide = tk.LabelFrame(None,text='System wide themes/modes')
    SystemWideSpectrumCycle = tk.Button(SystemWide,text='Spectrum Cycling (broken)')
    SystemWideSpectrumCycle.bind('<Button-1>',CSChander)
    SystemWideSpectrumCycle.pack(side='left')
    SystemWideRainbow = tk.Button(SystemWide,text='Rainbow')
    SystemWideRainbow.bind('<Button-1>',CRBhander)
    SystemWideRainbow.pack(side='left')
    SystemWide.pack(anchor='se')

    OpenRGB_FX.mainloop()

#------Color Button Handlers---------
def CSChander(event):
    CSCProc = threading.Thread(group=None,target=CustomSpectrumCycle(),name='RGBEffectsBackGroundTask')
    CSCProc.daemon = True
    CSCProc.start()
    return

def CRBhander(event):
    CRBProc = threading.Thread(group=None,target=CustomRainbow(),name='RGBEffectsBackGroundTask')
    CRBProc.daemon = True
    CRBProc.start()
    return

CustomRainbow()