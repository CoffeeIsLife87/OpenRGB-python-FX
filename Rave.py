import colorsys, random, string, sys, multiprocessing, time, os, openrgb
from openrgb.utils import DeviceType, ModeData, RGBColor, ZoneType

# or the name could also be 'The Acid's Kickin In Hard' if you want (as per @Saint Mischievous on discord)

Black = RGBColor(0, 0, 0)

def UserInput():
    """It will always return 5 things;\n
    Color1, Color2, Speed, Devices for reversal, Devices that are enables"""
    Color1 = Color2 = Speed = ReversedDevice = OnlySet = None
    for arg in sys.argv:
        if arg == '--C1':
            Pos = sys.argv.index(arg) + 1
            R, G, B = sys.argv[Pos:(Pos + 3)]
            Color1 = RGBColor(int(R),int(G),int(B))
        elif arg == '--C2':
            Pos = sys.argv.index(arg) + 1
            R, G, B = sys.argv[Pos:(Pos + 3)]
            Color2 = RGBColor(int(R),int(G),int(B))
        elif arg == '--reversed':
            ReversedDevices = (sys.argv.index(arg) + 1) # Will point to where the device(s) that need to be reversed are
            ReversedDevice = []
            if ' , ' in sys.argv[ReversedDevices]:
                for i in sys.argv[ReversedDevices].split(' , '):
                    for D in client.devices:
                        if D.name.strip().casefold() == i.strip().casefold():
                            ReversedDevice += [D]
            else:
                for D in client.devices:
                    if D.name.strip().casefold() == sys.argv[ReversedDevices].strip().casefold():
                        ReversedDevice += [D]
        elif arg == '--only-set':
            AllowedDevices = (sys.argv.index(arg) + 1) # Will point to where the device(s) that are allowed are
            OnlySet = []
            if ' , ' in sys.argv[AllowedDevices]:
                for i in sys.argv[AllowedDevices].split(' , '):
                    for D in client.devices:
                        if D.name.strip().casefold() == i.strip().casefold():
                            OnlySet += [D]
            else:
                for D in client.devices:
                    if D.name.strip().casefold() == sys.argv[AllowedDevices].strip().casefold():
                        OnlySet += [D]
        elif arg == '--speed':
            Speed = int(sys.argv[(sys.argv.index(arg) + 1)])
        else:
            pass
    return(Color1, Color2, Speed, ReversedDevice, OnlySet)

class ColorDrop:
    """
    Connects to an OpenRGB device and displays a rain effect.
    """
    def __init__(self, device_index, surface_index, InstColor, ReverseBool):
        self.Color = InstColor
        self.device = None
        client = openrgb.OpenRGBClient()
        self.device = client.devices[device_index]
        self.surface = self.device.zones[surface_index]
        if self.surface.type != ZoneType.LINEAR:
            raise Exception("not a linear zone")

        if ReverseBool == True:
            self.surface.leds.reverse()
        elif ReverseBool == False:
            self.surface.leds
        
        self.leds = self.surface.leds
        self.set_mode()

    def set_mode(self):
        """
        Set in a direct / static mode.
        """
        try:
            self.device.set_mode('direct')
        except:
            try:
                self.device.set_mode('static')
                print("error setting %s\nfalling back to static" %
                      self.device.name)
            except:
                print(
                    "Critical error! couldn't set %s to static or direct" %
                    self.device.name)
        self.device.set_color(Black)

    @staticmethod
    def transformer(state, ratio):
        """
        Apply the rain transformation to this `state`
        """
        transformed = []
        for i in range(0, len(state)):
            if i == 0:
                # Mutation goes here
                x = random.randint(0, len(state)*ratio) == 0
                if state[0] and not state[1]:
                    x = True
            else:
                x = state[i-1]
            transformed.append(x)
        return transformed

    def start(self, refresh=30, ratio=10):
        """
        Start the effect on this surface.
        """
        state = [False for _ in self.leds]
        prev_state = state
        while True:
            for i, value in enumerate(state):
                try:
                    if prev_state[i] != value:
                        # smooth it out
                        self.leds[i].set_color(
                            {
                                True: self.Color,
                                False: Black
                            }[value]
                        )
                except ValueError:
                    return

            prev_state = state.copy()
            state = ColorDrop.transformer(state, ratio)
            time.sleep(1.0/refresh)

def Setup_Drop(device_idx, surface_idx, InstColor, ReverseBool):
    """
    Creates and instance of the SurfaceRain object and starts it.
    Used by threads to provide a nice interface to do this.
    """
    inst = ColorDrop(device_idx, surface_idx, InstColor, ReverseBool)
    inst.start(ratio=10)

if __name__ == "__main__":
    Clist = [RGBColor(255,255,0),RGBColor(0, 255, 100),RGBColor(0, 255, 255),RGBColor(255,0,100),RGBColor(100,0,255)]
    CName = ['Yellow','Aqua','Cyan','Red','DarkPurple']
    # Get a list of surfaces
    client = openrgb.OpenRGBClient()

    _, _, _, Reversed, Enabled = UserInput()

    Enable = []
    if Enabled == None:
        Enable += [i for i in client.devices]
    elif Enabled != None:
        Enable = Enabled
    
    for C in Clist:
        surfaces = []
        for device_idx, device in enumerate(Enable):
            if Reversed != None:
                for R in Reversed:
                    if R == device:
                        ReverseBool = True
                        continue
                    else:
                        ReverseBool = False
            else:
                ReverseBool = False
            for zone_idx, zone in enumerate(device.zones):
                if zone.type == ZoneType.LINEAR:
                    surfaces.append((device_idx, zone_idx, C, ReverseBool))

        for surface in surfaces:
            t = multiprocessing.Process(name="%s%s"%(zone.name,CName[Clist.index(C)]), target=Setup_Drop, args=surface)
            t.start()