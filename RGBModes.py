
# an entry contains the following
# All possible modes
# The equivelent of Rainbow
# The equivelent of cycling
# The equivelent of static
# more modes might be added but these are the ones that I think people will use the most

def SupportedModes(Device , Request):
    #MotherBoards
    if Device == 'ASRock Polychrome FW 3.04':
        Modes = ('off','static','breathing','strobe','spectrum cycle','random','wave','spring','stack','cram','scan','neon','water','rainbow')
        rainbow = 'rainbow'
        cycling = 'wave'
        static = 'static'
    #CPU coolers
    #RAM
    if Device == 'Corsair Vengeance Pro RGB':
        Modes = ('off','direct','color shift','color pulse','rainbow wave','color wave','visor','rain','marquee','rainbow','sequential')
        rainbow = 'rainbow wave'
        cycling = 'rainbow'
        static = 'direct'
    #GPU's
    #LED strips
    #headsets
    #Headset Stands
    #Keyboards
    #mice
    if Device == 'Razer DeathAdder Elite':
        Modes = ('off','direct','static','breathing','spectrum cycling','reactive')
        rainbow = 'off'
        cycling = 'spectrum cycle'
        static = 'static'
    #Mouse Mats
    if Request == 'possible':
        return Modes
    if Request == 'rainbow':
        return rainbow
    if Request == 'cycling':
        return cycling
    if Request == 'static':
        return static