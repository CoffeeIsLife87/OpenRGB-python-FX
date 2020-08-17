import numpy as np

def SupportedARGB():
    Periferals = ['T-force Delta Max RGB']
    return Periferals

def GetPeriferalInfo(Periferal):
    if Periferal == 'T-force Delta Max RGB':
        Leds = np.zeros((10,8),int)
        Leds[0:10,0:1] = np.arange(0,10).reshape(10,1)
        Leds[0:10,7:8] = np.arange(19,9,-1).reshape(10,1)
        Leds[0:10,1:7] = '-1'
        print(Leds)
GetPeriferalInfo('T-force Delta Max RGB')