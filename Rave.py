import colorsys, random, string, sys, multiprocessing, time, os, openrgb
from openrgb.utils import DeviceType, ModeData, RGBColor, ZoneType

# or the name could also be 'The Acid's Kickin In Hard' if you want (as per @Saint Mischievous on discord)

def set_mode():
    for device in client.devices:
        try:
            device.set_mode('direct')
        except:
            try:
                device.set_mode('static')
                print("error setting %s\nfalling back to static" %device.name)
            except:
                print("Critical error! couldn't set %s to static or direct" %device.name)
        device.set_color(Black)

Black = RGBColor(0, 0, 0)
class ColorDrop:
    """
    Connects to an OpenRGB device and displays a rain effect.
    """
    def __init__(self, device_index, surface_index, InstColor):
        self.Color = InstColor
        self.device = None
        client = openrgb.OpenRGBClient()
        self.device = client.devices[device_index]
        self.surface = self.device.zones[surface_index]
        if self.surface.type != ZoneType.LINEAR:
            raise Exception("not a linear zone")
        self.surface.leds.reverse()
        self.leds = self.surface.leds
    
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

def Setup_Drop(device_idx, surface_idx, InstColor):
    """
    Creates and instance of the SurfaceRain object and starts it.
    Used by threads to provide a nice interface to do this.
    """
    inst = ColorDrop(device_idx, surface_idx, InstColor)
    inst.start(ratio=10)

Clist = [RGBColor(255,255,0),RGBColor(0, 255, 100),RGBColor(0, 255, 255),RGBColor(255,0,100),RGBColor(100,0,255)]
CName = ['Yellow','Aqua','Cyan','Red','DarkPurple']

client = openrgb.OpenRGBClient()
# Get a list of surfaces
if __name__ == '__main__':
    set_mode()
    for C in Clist:
        surfaces = []
        for device_idx, device in enumerate(client.devices):
            for zone_idx, zone in enumerate(device.zones):
                if zone.type == ZoneType.LINEAR:
                    surfaces.append((device_idx, zone_idx, C))

        for surface in surfaces:
            t = multiprocessing.Process(name="%s%s"%(zone.name,CName[Clist.index(C)]), target=Setup_Drop, args=surface)
            t.start()