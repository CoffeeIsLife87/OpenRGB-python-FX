import FX , RGBModes
import tkinter as tk
from LightIndexes import GetIndex

ModeList = [[]]
check = 0

def FormGUI():

    OpenRGB_FX = tk.Tk(screenName='OpenRGB FX',baseName='OpenRGB FX')
    OpenRGB_FX.minsize(600,400)
    OpenRGB_FX.title('OpenRGB FX')

    #------------------------------------ Set Specific Device, Mode, and Color
    def MakeDeviceFrame():#in VScode functions are colapsable so that is why this is how it is
        DLocations = tk.Frame(None,width=300,height=300)
        DLocations.pack(anchor='ne')
        #for Device in FX.Dlist:
        #    DLayout = GetIndex.Index(Device.name)
        #    print(DLayout)
    MakeDeviceFrame()

    SpecificDeviceFrame = tk.Frame(None)

    CurrentDevice = tk.StringVar(SpecificDeviceFrame)

    for Device in FX.Dlist:
        try:
            DeviceList = DeviceList + [Device.name]
        except:
            DeviceList = [Device.name]

    DSubFrame = tk.Frame(SpecificDeviceFrame)

    ModeVar = tk.Variable(SpecificDeviceFrame)
    global check
    if check == 0:
        ModeMenu = tk.OptionMenu(DSubFrame,ModeVar,*ModeList)
        check += 1

    def ListEventHandler(event):
        NewModeList = (RGBModes.SupportedModes(CurrentDevice.get(),'possible'))

        def Refresh():
            ModeVar.set('')
            ModeMenu['menu'].delete(0,'end')

            if str(type(NewModeList)) != "<class 'NoneType'>":
                for Mode in NewModeList:
                    ModeMenu['menu'].add_command(label=Mode, command=tk._setit(ModeVar, Mode))
        Refresh()
    
    ModeMenu = tk.OptionMenu(DSubFrame,ModeVar,*ModeList)
    ModeMenu.pack(side='left')
    
    ApplyMode = tk.Button(DSubFrame,text='Apply',command=lambda: Apply(ModeVar,CurrentDevice))

    ApplyMode.pack(side='right')
    DSubFrame.pack(side='bottom')


    DeviceMenu = tk.OptionMenu(SpecificDeviceFrame,CurrentDevice,*DeviceList,command=(ListEventHandler))
    DeviceMenu.pack(side='top')

    
    
    SpecificDeviceFrame.pack(side='left')

    #------------------------------------ Presets (set all devices)
    SetModeFrame = tk.LabelFrame(None,text='Set Mode to')
    StaticButton = tk.Button(SetModeFrame,text='Static')
    StaticButton.bind('<Button-1>',StaticButtonHandler)
    StaticButton.pack(side='left')

    SpectrumCycleButton = tk.Button(SetModeFrame,text='Spectrum Cycling')
    SpectrumCycleButton.bind('<Button-1>',SpectrumCycleButtonHandler)
    SpectrumCycleButton.pack(side='left')
    
    RainbowButton = tk.Button(SetModeFrame,text='Rainbow')
    RainbowButton.bind('<Button-1>',RainbowButtonHandler)
    RainbowButton.pack(side='left')
    SetModeFrame.pack(side='bottom')

    OpenRGB_FX.mainloop()

def Apply(ModeVar,CurrentDevice):
    Mode = ModeVar.get()
    Device = CurrentDevice.get()
    FX.SetSpecific(Mode,Device)

def RainbowButtonHandler(event):
    FX.SetMode('rainbow')

def StaticButtonHandler(event):
    FX.SetMode('static')

def SpectrumCycleButtonHandler(event):
    FX.SpectrumCycle()

FormGUI()