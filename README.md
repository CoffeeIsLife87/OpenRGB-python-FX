# OpenRGB-python-FX

## Effect List

* Rainbow wave (now speed controllable but is buggy for some speeds)

* Spectrum cycling (Credit to James Potkukelkka on discord for this one)

* Gradient cycling

* Breathing

* Ambient (credit to usrErr0r on discord for this one, Not working on linux due to ImageGrab not having an import)

* Rain (**Massive** thanks and credit to Bahorn on discord for this one)

* Cram

* Chase (Per request of Titanium on Discord)

* Rave (Basically multiple instances of rain with different colors that make a cool effect, Discovered by Saint Mischievous on discord)

## Usage

* start the openRGB sdk server, otherwise this *will not work*

* you may need to install the sdk binding ```pip install openrgb-python``` or ```pip3 install openrgb-python``` (you may also need to add --user at the end for linux)

* clone the repository or download the effect you want

* cd into the folder with the python files

* run using ```python3 file.py``` or ```python file.py```

* enjoy the effect :)

### usage note

* Some effects support custom colors (gradcycle, breathing, and rain)

  * To use custom colors you must have 3(for breathing) or 6(for gradcycle) numbers ranging 0 to 255

  * something like ```python(3) gradcycle.py 0 255 255 255 30 0``` or ```python(3) breathing.py 0 255 90```

* Ambient requires some special python modules

  * ```pip install pillow colour``` or ```pip3 install pillow colour``` (again, you may also need to add ```--user``` to the end for it to work)

* For effects that have custom speeds, the speed comes before the color (``python Breathing 5(speed) 255 0 0(color)``)

## Writing effects

Effects are stored in their own .py file for now

```
import openrgb , time , string , colorsys , sys
from openrgb.utils import RGBColor , ModeData , DeviceType , ZoneType

client = openrgb.OpenRGBClient()

Dlist = client.devices
```

is a good starting point

## Notes

While this is system wide, there are some limitations.

if the device isn't in openRGB then the effect *will not* apply to it

currently rainbow is poorly optimized due to a lack of big brainedness on my part (I did do some optimizations that allows me to use .show() and that made it more readable for other people)

Ambient grabs the entire screen leading to some shade of white or black. hopefully this will get fixed soon

The ReWrite of GradCycle and Rainbow are done so they are fully functional

## Todo

* Make effects reversable (some ram leds are in a different order than others)
  * Add a toggle for device names

  * Add it into the ``while True:`` loops

* Make contributing easier (more templates and comments/doc strings)

* Add matrix zone support for some effects (rainbow wave and gradcycle)

* Smooth out some of the effects (rainbow wave)

* Create GUI for launching effects (most effects are built as functions so incorporating them wouldn't be that hard)
