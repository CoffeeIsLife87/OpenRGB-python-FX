# As of now all the code in this file is by bahorn with some minor modifications (moving stuff) by me
import colorsys, random, string, sys, multiprocessing, time, os, openrgb
from openrgb.utils import DeviceType, ModeData, RGBColor, ZoneType

Black = RGBColor(0, 0, 0)

# Check for user selected color
if len(sys.argv) == 4:
    Color = RGBColor(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
else:
    Color = RGBColor(255,0,0)

class SurfaceRain:
    """
    Connects to an OpenRGB device and displays a rain effect.
    """
    def __init__(self, device_index, surface_index):
        self.device = None
        client = openrgb.OpenRGBClient()
        self.device = client.devices[device_index]

        self.surface = self.device.zones[surface_index]
        if self.surface.type != ZoneType.LINEAR:
            raise Exception("not a linear zone")


        self.surface.leds.reverse()
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
                                True: Color,
                                False: Black
                            }[value]
                        )
                except ValueError:
                    return

            prev_state = state.copy()
            state = SurfaceRain.transformer(state, ratio)
            time.sleep(1.0/refresh)

def setup_rain(device_idx, surface_idx):
    """
    Creates and instance of the SurfaceRain object and starts it.
    Used by threads to provide a nice interface to do this.
    """
    inst = SurfaceRain(device_idx, surface_idx)
    inst.start(ratio=10)

if __name__ == "__main__":
    # Get a list of surfaces
    client = openrgb.OpenRGBClient()
    surfaces = []
    for device_idx, device in enumerate(client.devices):
        for zone_idx, zone in enumerate(device.zones):
            if zone.type == ZoneType.LINEAR:
                surfaces.append((device_idx, zone_idx))
    del client
    for surface in surfaces:
        t = multiprocessing.Process(target=setup_rain, args=surface)
        t.start()