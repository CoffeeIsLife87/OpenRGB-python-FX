import RGBModes , threading , openrgb , time , string , multiprocessing
from openrgb.utils import DeviceType , RGBColor , ModeData
from LightIndexes import GetIndex
from tkinter import colorchooser
import tkinter as tk

client = openrgb.OpenRGBClient()

Dlist = client.devices

def Apply(ModeVar,CurrentDevice,C):
    _ , DeviceID = CurrentDevice.get().split(' (')
    DeviceID , _ = DeviceID.split(')')
    print(DeviceID)
    Mode = ModeVar.get()
    SetSpecific(Mode,DeviceID,Color=C)

def SetDeviceColors(DeviceID, R , G , B):#device, R , G , B):
    if DeviceID == 'all':
        for i in Dlist:
            if i.name != 'ASRock Polychrome FW 3.255':
                #print(i.id)
                i.set_color(RGBColor(R,G,B))
                time.sleep(0.0003)
        return
    else:
        for i in Dlist:
            if i.id == int(DeviceID):
                i.set_color(RGBColor(R,G,B))
                return

def wait():
    time.sleep(0.003)

def DebugRGB(R , G , B):# for printing the values that are being set
    Debug = 0
    if Debug == 1:
        print(R , G , B)
    else:
        return

def SetSpecific(Mode , DeviceID , Color=(0,0,255), Speed=(1) , Direction='down'):
    for D in Dlist:
        if D.id == int(DeviceID):
            try:
                Mode.speed = Speed
            except:
                pass
            try:
                Mode.Direction(Direction)
            except:
                pass
            D.set_mode(Mode)
            R = int(Color[0][0])
            G = int(Color[0][1])
            B = int(Color[0][2])
            SetDeviceColors(DeviceID , R,G,B)

def SetMode(Mode,color=(255,0,0),speed=1,Direction='down'):
    for Device in client.devices:
        if Device.name != 'ASRock Polychrome FW 3.255':
            try:
                Device.set_mode(RGBModes.SupportedModes(Device.name,Mode))
            except:
                print('Unable to set %s'%Device.name)

def CustomSpectrumCycle(CycleSpeed=''):
    SetMode('static')
    CycleSpeed = 3
    R = G = B = 0
    RedoLoop = 0
    while 1 == 1:
        if RedoLoop == 1:
            RedoLoop = 0
        R += CycleSpeed
        DebugRGB(R , G , B)
        SetDeviceColors('all' , R , G , B)
        time.sleep(0.002)
        if R == 255:
            while 1 == 1:
                if RedoLoop == 1:
                    break
                G += CycleSpeed
                DebugRGB(R , G , B)
                SetDeviceColors('all' , R , G , B)
                time.sleep(0.002)
                if G == 255:
                    while 1 == 1:
                        if RedoLoop == 1:
                            break
                        R -= CycleSpeed
                        DebugRGB(R , G , B)
                        SetDeviceColors('all' , R , G , B)
                        time.sleep(0.002)
                        if R == 0:
                            while 1 == 1:
                                if RedoLoop == 1:
                                    break
                                B += CycleSpeed
                                DebugRGB(R , G , B)
                                SetDeviceColors('all' , R , G , B)
                                time.sleep(0.002)
                                if B == 255:
                                    while 1 == 1:
                                        if RedoLoop == 1:
                                            break
                                        G -= CycleSpeed
                                        DebugRGB(R , G , B)
                                        SetDeviceColors('all' , R , G , B)
                                        time.sleep(0.002)
                                        if G == 0:
                                            while 1 == 1:
                                                if RedoLoop == 1:
                                                    break
                                                R += CycleSpeed
                                                DebugRGB(R , G , B)
                                                SetDeviceColors('all' , R , G , B)
                                                time.sleep(0.002)
                                                if R == 255:
                                                    while 1 == 1:
                                                        if RedoLoop == 1:
                                                            break
                                                        B -= CycleSpeed
                                                        DebugRGB(R , G , B)
                                                        SetDeviceColors('all' , R , G , B)
                                                        time.sleep(0.002)
                                                        if B == 0:
                                                            while 1 == 1:
                                                                if RedoLoop == 1:
                                                                    break
                                                                G += CycleSpeed
                                                                B += CycleSpeed
                                                                DebugRGB(R , G , B)
                                                                SetDeviceColors('all' , R , G , B)
                                                                time.sleep(0.002)
                                                                if (str(R) + str(G) + str(B)) == "255255255":
                                                                    while 1 == 1:
                                                                        R -= CycleSpeed
                                                                        G -= CycleSpeed
                                                                        B -= CycleSpeed
                                                                        DebugRGB(R , G , B)
                                                                        SetDeviceColors('all' , R , G , B)
                                                                        time.sleep(0.002)
                                                                        if B == 0:
                                                                            RedoLoop = 1
                                                                            break

ModeList = [[]]
check = 0
RamNum = 0
def FormGUI():

    OpenRGB_FX = tk.Tk(screenName='OpenRGB FX',baseName='OpenRGB FX')
    OpenRGB_FX.minsize(600,400)
    OpenRGB_FX.title('OpenRGB FX')

    #------Device Frame---------
    DLocations = tk.LabelFrame(None,width=300,height=300,bg='#3c423d')
    RamZone = tk.Frame(master=DLocations,width=80,height=180)
    DimmOne = tk.Frame(master=RamZone,width=20,height=180,padx=3)#,bg='black')
    DimmTwo = tk.Frame(master=RamZone,width=20,height=180,padx=3)
    DimmThree = tk.Frame(master=RamZone,width=20,height=180,padx=3)#,bg='black')
    DimmFour = tk.Frame(master=RamZone,width=20,height=180,padx=3)
    
    #RamColorButton = tk.Button(DLocations,text='Ram Button',command=lambda: (DimmOne.!labelframe.LED0.config(bg='blue')) )
    # I am trying to set a frame color but said frame is declaired in a different file and returned to this one
    # but it does appear in the GUI so I assume it is still loaded into memory and editable
    # So I want to do something like "DimmOne.RamDimm.LED0.bg = 'blue'"
    #RamColorButton.pack()

    def MakeRamLeds():
        global RamNum
        for Device in Dlist:
            if Device.type == DeviceType.DEVICE_TYPE_DRAM:
                RamNum += 1
                if RamNum == 1:
                    GetIndex.Index(Device.name,DimmOne)
                if RamNum == 2:
                    GetIndex.Index(Device.name,DimmTwo)
                if RamNum == 3:
                    GetIndex.Index(Device.name,DimmThree)
                if RamNum == 4:
                    GetIndex.Index(Device.name,DimmFour)
    MakeRamLeds()
    DimmOne.pack(side='left')
    DimmTwo.pack(side='left')
    DimmThree.pack(side='left')
    DimmFour.pack(side='left')
    RamZone.pack()
    DLocations.pack(anchor='ne')
    
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
        NewModeList = (RGBModes.SupportedModes(DeviceName,'possible'))

        def Refresh():
            ModeVar.set('')
            ModeMenu['menu'].delete(0,'end')

            if str(type(NewModeList)) != "<class 'NoneType'>":
                for Mode in NewModeList:
                    ModeMenu['menu'].add_command(label=Mode, command=tk._setit(ModeVar, Mode))
        Refresh()
    
    #------RGB controller presets (non custom)---------
    ModeMenu = tk.OptionMenu(DSubFrame,ModeVar,*ModeList)
    ModeMenu.pack(side='left')
    
    def GetColor():
        global RGBValue
        Color = colorchooser.askcolor
        RGBValue = Color()

    ColorButton = tk.Button(DSubFrame,text='Pick Color',command=GetColor)
    ColorButton.pack(side='left')
    
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
    SetModeFrame.pack(anchor='se')

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
    SystemWide.pack(anchor='se')

    OpenRGB_FX.mainloop()

#------Color Button Handlers---------
def RainbowButtonHandler(event):
    SetMode('rainbow')

def StaticButtonHandler(event):
    SetMode('static')

def SpectrumCycleButtonHandler(event):
    SetMode('cycling')

def CSChander(event):
    CSCProc = threading.Thread(group=None,target=CustomSpectrumCycle(),name='RGBeffectsBackGroundTask')
    CSCProc.daemon = True
    CSCProc.start()
    return

FormGUI()