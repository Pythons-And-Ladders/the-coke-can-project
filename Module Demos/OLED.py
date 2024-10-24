from machine import Pin, I2C
import sh1106
import time

# Define I2C pins for TTGO T-BEAM S3 bus 0
SDA = Pin(17)  # SDA pin
SCL = Pin(18)  # SCL pin

# Create I2C interface
I2C_BUS0 = I2C(0, scl=SCL, sda=SDA, freq=400000)

# Initialise the SH1106 OLED display (128x64 resolution)
OLED = sh1106.SH1106_I2C(128, 64, I2C_BUS0)

# Clear the display
OLED.fill(0)

# Display text. text function is formatted such that OLED.text([text], [distance from left], [distance from top])
OLED.text("Testing123", 0, 0)

# Update the display to show the text
OLED.show()
