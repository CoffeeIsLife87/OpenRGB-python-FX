import FX
import tkinter as tk

def FormGUI():

    OpenRGB_FX = tk.Tk(screenName='OpenRGB FX',baseName='OpenRGB FX')
    OpenRGB_FX.minsize(600,400)
    OpenRGB_FX.title('OpenRGB FX')

    SetModeFrame = tk.LabelFrame(None,text='Set Mode to')#,size=(200,200))

    StaticButton = tk.Button(SetModeFrame,text='Static')
    StaticButton.bind('<Button-1>',StaticButtonHandler)
    StaticButton.pack()

    SpectrumCycleButton = tk.Button(SetModeFrame,text='Spectrum Cycling')
    SpectrumCycleButton.bind('<Button-1>',SpectrumCycleButtonHandler)
    SpectrumCycleButton.pack()
    
    SetModeFrame.pack()

    OpenRGB_FX.mainloop()

def StaticButtonHandler(event):
    FX.SetMode('static')

def SpectrumCycleButtonHandler(event):
    FX.SpectrumCycle()

FormGUI()
