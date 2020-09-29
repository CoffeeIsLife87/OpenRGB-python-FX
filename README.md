# OpenRGB-python-FX

## Effect List

* Rainbow wave

* Spectrum cycling

* Gradient cycling

* Breathing

## Usage

* start the openRGB sdk server, otherwise this *will not work*

* you may need to install the sdk binding ```pip install openrgb-python``` or ```pip3 install openrgb-python``` (you may also need to add --user at the end for linux)

* clone the repository or download the effect you want

* run using ```python3 file.py``` or ```python file.py```

* enjoy the effect :)

### usage note

Some effects support custom colors (gradcycle and breathing)

To use custom colors you must have 3(for breathing) or 6(for gradcycle) numbers ranging 0 to 255

something like ```python(3) gradcycle.py 0 255 255 255 30 0``` or ```python(3) breathing.py 0 255 90```


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

currently rainbow is poorly optimized due to a python sdk binding issue so it might be a bit jarring
