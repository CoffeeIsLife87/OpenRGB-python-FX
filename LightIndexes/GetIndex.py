import importlib

def HasIndex(CompName):
    #print(CompName)
    Comp = CompName.replace(' ','')
    Comp = ("LightIndexes.%s"%Comp)
    try:
        Device = importlib.__import__(Comp,fromlist=('LightIndexes'))
        LEDmap = Device.ReturnStats()
        return(LEDmap)
    except ImportError:
        return ('No Light index for %s'%CompName)
