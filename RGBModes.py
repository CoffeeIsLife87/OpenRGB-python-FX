def SupportedModes(Device):
    #MotherBoards
    if Device == 'ASRock Polychrome FW 3.04':
        Modes = ('off','static','breathing','strobe','spectrum cycle','random','wave','spring','stack','cram','scan','neon','water','rainbow')
    #CPU coolers
    #RAM
    if Device == 'Corsair Vengeance Pro RGB':
        Modes = ('off','direct','color shift','color pulse','rainbow wave','color wave','visor','rain','marquee','rainbow','sequential')
    #GPU's
    #LED strips
    #headsets
    #Headset Stands
    #Keyboards
    #mice
    if Device == 'Razer DeathAdder Elite':
        Modes = ('off','direct','static','breathing','spectrum cycling','reactive')
    #Mouse Mats
    return Modes