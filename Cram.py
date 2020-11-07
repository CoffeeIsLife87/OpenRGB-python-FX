import openrgb , time , sys , random
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

if len(sys.argv) == 4:
    Color = RGBColor(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
else:
    Color = 0

def RandomColor(MinVal=200):
    """
    MinVal will be the smallest number you are ok with
    The higher the number, the brighter the resulting color will be
    """
    while True:
        CR = random.randint(0,255)
        CG = random.randint(0,255)
        CB = random.randint(0,255)
        if (CR + CG + CB) >= MinVal:
            return CR, CG, CB

Check = 0
for i in Dlist:
    Bigger = len(i.leds)
    if Check < Bigger:
        Check = Bigger

while True:
    Num = 0
    if Color == 0:
        R, G, B = RandomColor()
        NewColor = RGBColor(R,G,B)
    else:
        NewColor = Color
    while Num < Check:
        for Device in Dlist:
            try:
                Device.leds[Num].set_color(NewColor)
            except:
                pass
        Num += 1
        time.sleep(0.1)
    time.sleep(1)
    for Device in Dlist:
        Device.set_color(RGBColor(0,0,0))
        time.sleep(0.01)
    time.sleep(0.5)
