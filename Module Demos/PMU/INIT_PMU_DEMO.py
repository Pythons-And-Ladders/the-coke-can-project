from AXP2101 import *
from machine import Pin, I2C

# Define pins and initialise I2C bus
SDA = 42
SCL = 41
I2C_BUS1 = I2C(1, scl=Pin(SCL), sda=Pin(SDA))

# Initialise the PMU object with I2C bus
PMU = AXP2101(I2C_BUS1, addr=AXP2101_SLAVE_ADDRESS)

# Check if the PMU is connected and working
id = PMU.getChipID()
if id != XPOWERS_AXP2101_CHIP_ID:
    print("PMU is not online...")
else:
    print('PMU initialised, Chip ID: {}'.format(hex(id)))
