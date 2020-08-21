import importlib

def Index(CompName,RamNum=1):
    #print(CompName)
    Comp = CompName.replace(' ','')
    Comp = ("LightIndexes.%s"%Comp)
    #try:
    Device = importlib.__import__(Comp,fromlist=('LightIndexes'))
    #LEDmap = Device.ReturnStats()
    LEDmap = Device.ReturnRamLEDMap(RamNum)
    return(LEDmap)
    #except ImportError:
    #    return ('No Light index for %s'%CompName)
