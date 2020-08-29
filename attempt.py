import tkinter as tk
import threading
App = tk.Tk('RGB')
App.minsize(800,100)

LEDGroup = []
check = 0
while check < 20:
    LEDGroup = LEDGroup + [tk.Frame(App,width=40,height=100,background='black')]
    check += 1

Button = tk.Button(text='yes',command=(lambda: CSCButton()))
Button.pack()

for i in LEDGroup:
    i.pack(side='left')

def CSCButton():
    CustomSpectrumCycle()
    T = threading.Thread(CustomSpectrumCycle(),daemon=False)
    T.start()

def RGBToHex(R,G,B):
    HexVal = ('#%02x%02x%02x' % (R, G, B))
    return(HexVal)

def SetDeviceColors(R,G,B):
    for i in LEDGroup:
        i['background'] = RGBToHex(R,G,B)

def CustomSpectrumCycle(CycleSpeed=3):#
    #SetStatic()
    R = G = B = 0
    RedoLoop = 0
    while 1 == 1:
        if RedoLoop == 1:
            RedoLoop = 0
        R += CycleSpeed
        SetDeviceColors(R , G , B)
        if R == 255:
            while 1 == 1:
                if RedoLoop == 1:
                    break
                G += CycleSpeed
                SetDeviceColors(R , G , B)
                if G == 255:
                    while 1 == 1:
                        if RedoLoop == 1:
                            break
                        R -= CycleSpeed
                        SetDeviceColors(R , G , B)
                        if R == 0:
                            while 1 == 1:
                                if RedoLoop == 1:
                                    break
                                B += CycleSpeed
                                SetDeviceColors(R , G , B)
                                if B == 255:
                                    while 1 == 1:
                                        if RedoLoop == 1:
                                            break
                                        G -= CycleSpeed
                                        SetDeviceColors(R , G , B)
                                        if G == 0:
                                            while 1 == 1:
                                                if RedoLoop == 1:
                                                    break
                                                R += CycleSpeed
                                                SetDeviceColors(R , G , B)
                                                if R == 255:
                                                    while 1 == 1:
                                                        if RedoLoop == 1:
                                                            break
                                                        B -= CycleSpeed
                                                        SetDeviceColors(R , G , B)
                                                        if B == 0:
                                                            while 1 == 1:
                                                                if RedoLoop == 1:
                                                                    break
                                                                G += CycleSpeed
                                                                B += CycleSpeed
                                                                SetDeviceColors(R , G , B)
                                                                if (str(R) + str(G) + str(B)) == "255255255":
                                                                    while 1 == 1:
                                                                        R -= CycleSpeed
                                                                        G -= CycleSpeed
                                                                        B -= CycleSpeed
                                                                        SetDeviceColors(R , G , B)
                                                                        if B == 0:
                                                                            RedoLoop = 1
                                                                            break

#CustomSpectrumCycle()
App.mainloop()
