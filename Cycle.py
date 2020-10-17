import openrgb , time , string , colorsys
from openrgb.utils import RGBColor , ModeData

client = openrgb.OpenRGBClient()

Dlist = client.devices

def wait():
    time.sleep(0.003)

def SetStatic():
    for Device in client.devices:
        time.sleep(0.1)
        try:
            Device.set_mode('direct')
            print('Set %s successfully'%Device.name)
        except:
            try:
                Device.set_mode('static')
                print('error setting %s\nfalling back to static'%Device.name)
            except:
                print("Critical error! couldn't set %s to static or direct"%Device.name)
SetStatic()

def CustomSpectrumCycle(CycleSpeed=1000):#
    SetStatic()
    while True:
        #credit to @James Potkukelkka on discord for MOST of the code
        hue_range = CycleSpeed # Smaller = faster
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

CustomSpectrumCycle()