import openrgb , time , string , colorsys , sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices

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


def MakeCBase(StartingColor=None,EndingColor=None):
    def hex_to_RGB(hex):
      ''' "#FFFFFF" -> [255,255,255] '''
      # Pass 16 to the integer function for change of base
      return [int(hex[i:i+2], 16) for i in range(1,6,2)]

    def RGB_to_hex(RGB):
      ''' [255,255,255] -> "#FFFFFF" '''
      # Components need to be integers for hex to make sense
      RGB = [int(x) for x in RGB]
      return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                "{0:x}".format(v) for v in RGB])

    def color_dict(gradient):
      ''' Takes in a list of RGB sub-lists and returns dictionary of
        colors in RGB and hex form for use in a graphing function
        defined later on '''
      return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
          "r":[RGB[0] for RGB in gradient],
          "g":[RGB[1] for RGB in gradient],
          "b":[RGB[2] for RGB in gradient]}

    def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
      ''' returns a gradient list of (n) colors between
        two hex colors. start_hex and finish_hex
        should be the full six-digit color string,
        inlcuding the number sign ("#FFFFFF") '''
      # Starting and ending colors in RGB form
      s = hex_to_RGB(start_hex)
      f = hex_to_RGB(finish_hex)
      # Initilize a list of the output colors with the starting color
      RGB_list = [s]
      # Calcuate a color at each evenly spaced value of t from 1 to n
      for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
          int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
          for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

      return color_dict(RGB_list)

    def polylinear_gradient(colors, n):
      ''' returns a list of colors forming linear gradients between
          all sequential pairs of colors. "n" specifies the total
          number of desired output colors '''
      # The number of colors per individual linear gradient
      n_out = int(float(n) / (len(colors) - 1))
      # returns dictionary defined by color_dict()
      gradient_dict = linear_gradient(colors[0], colors[1], n_out)

      if len(colors) > 1:
        for col in range(1, len(colors) - 1):
          next = linear_gradient(colors[col], colors[col+1], n_out)
          #for k in ("hex", "r", "g", "b"):
          for k in ("r", "g", "b"):
            # Exclude first point to avoid duplicates
            gradient_dict[k] += next[k][1:]

      return gradient_dict

    Grad = polylinear_gradient((RGB_to_hex(StartingColor),RGB_to_hex(EndingColor),RGB_to_hex(StartingColor)),255)

    RList , GList , BList = Grad['r'], Grad['g'], Grad['b']

    def FinishCbase(R , G , B):
        Cbase = []
        ListPos = 0
        while ListPos < len(R):
            C = (R[ListPos],G[ListPos],B[ListPos])
            Cbase = Cbase + [C]
            ListPos += 1
        return Cbase

    ColorBase = FinishCbase(RList,GList,BList)

    return ColorBase

def GradCycle(MaxOffset=15,speed=3,C1=(0,255,255),C2=(120,0,255)):

    for Device in Dlist:# set to direct or static as a fallback
        time.sleep(0.3)
        try:
            Device.set_mode('direct')
            print('Set %s successfully'%Device.name)
        except:
            try:
                print('error setting %s\nfalling back to static'%Device.name)
                Device.set_mode('static')
            except:
                print("Critical error! couldn't set %s to static or direct"%Device.name)
    
    Offset = 1
    CBase = MakeCBase(C1,C2)
    
    def wait():
        time.sleep(float('0.0%d'%speed))
    
    Zones = []
    num = 0

    for device in Dlist:
        for zone in device.zones:
            Zones = Zones + [[zone]]
            Offset = 2

            if zone.type == ZoneType.MATRIX:
                for SubZone in zone.matrix_map:
                    for led in SubZone:
                        if led != None:
                            Zones[num] = Zones[num] + [[[device.leds[led]], [Offset]]]

                    Offset += 1
            elif device.name == 'ASRock Polychrome V2':
                for led in reversed(zone.leds):
                    if len(zone.leds) == 1:
                        Offset = 5
                    Zones[num] = Zones[num] + [[[led],[Offset]]]
                    Offset += 1
                    
            else:
                for led in zone.leds:
                    Zones[num] = Zones[num] + [[[led],[Offset]]]
                    Offset += 1
            num += 1

    while True:
        wait()
        for Z in Zones:
            for LED in Z[1:]:
                Color = len(CBase)/MaxOffset
                try:
                    LEDColor = (int(Color)*LED[1][0])
                except:
                    print(LED)
                    exit()
                if LEDColor >= len(CBase):
                    LEDColor = len(CBase) -1
                CR , CB , CG = CBase[LEDColor]
                LED[0][0].set_color(RGBColor(CR , CB , CG))
                if LED[1][0] >= MaxOffset:
                    LED[1][0] = 1
                else:
                    LED[1][0] += 1

if len(sys.argv) == 7:
    GradCycle(C1=(sys.argv[1],sys.argv[2],sys.argv[3]), C2=(sys.argv[4],sys.argv[5],sys.argv[6]))
else:
    GradCycle()