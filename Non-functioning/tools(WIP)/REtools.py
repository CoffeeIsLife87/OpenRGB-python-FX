#import time
#from smbus2 import SMBus

#bus = SMBus(2) #bus that the mobo is on
#addr = 0x6a #address of the polychrome controller

#bus.write_block_data(addr, 0x30, (0x01 , 0x11))

#print(bus.read_block_data(addr,0x32))
#bus.write_block_data(addr, 0x32, (0x01, 0x02))

#TryNum = 14

#Y = (0xeb, 0xd2, 0x34)
#B = (0x45, 0x36, 0xba)
#H = 0x10
#while TryNum <= 100:
#    bus.write_block_data(addr, 0x31, (0x01 , H))
#    #print(H)
#    #print(hex(H))
#    if (TryNum % 2) == 0:
#        C = Y
#    elif (TryNum % 2) != 0:
#        C = B
#    bus.write_block_data(addr, 0x34, C)
#    H += 1
#    TryNum += 1
#    time.sleep(1)


# 19 is the ARGB header so above may be the induvidule LEDs
#ZoneSelected = 0x31
