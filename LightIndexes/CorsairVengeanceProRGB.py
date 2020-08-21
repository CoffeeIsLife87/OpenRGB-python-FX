import numpy as np
import tkinter as tk
def ReturnStats():
    LEDmap = np.arange(9,-1,-1)
    LEDmap = np.reshape(LEDmap,(10,1))
    return LEDmap

def ReturnRamLEDMap(Dimm):
    RamDimm = tk.Frame(Dimm,width=20,height=180)
    LED0 = tk.Frame(RamDimm,width=20,height=20,bg='black')
    LED0.pack(side='top')
    LED1 = tk.Frame(RamDimm,width=20,height=20,bg='white')
    LED1.pack(side='top')
    LED2 = tk.Frame(RamDimm,width=20,height=20,bg='black')
    LED2.pack(side='top')
    LED3 = tk.Frame(RamDimm,width=20,height=20,bg='white')
    LED3.pack(side='top')
    LED4 = tk.Frame(RamDimm,width=20,height=20,bg='black')
    LED4.pack(side='top')
    LED5 = tk.Frame(RamDimm,width=20,height=20,bg='white')
    LED5.pack(side='top')
    LED6 = tk.Frame(RamDimm,width=20,height=20,bg='black')
    LED6.pack(side='top')
    LED7 = tk.Frame(RamDimm,width=20,height=20,bg='white')
    LED7.pack(side='top')
    LED8 = tk.Frame(RamDimm,width=20,height=20,bg='black')
    LED8.pack(side='top')
    LED9 = tk.Frame(RamDimm,width=20,height=20,bg='white')
    LED9.pack(side='top')
    RamDimm.pack()