from machine import SPI, Pin
import machine
import sh1106
import time
from sx1262 import SX1262

# Pin assignments
cs_pin = Pin(10, Pin.OUT)  # Chip Select
rst_pin = Pin(5, Pin.OUT)  # Reset
gpio_pin = Pin(4, Pin.IN)  # DIO1
irq_pin = Pin(1, Pin.IN)   # IRQ pin

# Create SX1262 object
sx = SX1262(spi_bus=2, clk=12, mosi=11, miso=13, cs=cs_pin, irq=irq_pin, rst=rst_pin, gpio=gpio_pin)

# Reset the module
rst_pin.value(0)  # Set RST low
time.sleep(0.1)  # Wait for 100 ms
rst_pin.value(1)  # Set RST high
time.sleep(0.5)  # Wait for 500 ms

# Begin communication with SX1262
sx.begin(freq=868, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

print("Receiver initialized successfully.")

# Function to handle received messages
def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print('Received message:', msg, 'with status:', error)
        oled.fill(0)
        oled.text("Message received:", 0, 0)
        oled.text(f"{msg}", 0, 20)
        oled.show()  # Ensure the display is updated

# Set callback for receiving messages
sx.setBlockingCallback(False, cb)  # Use non-blocking callback

while True:
    time.sleep(1)  # Keep the loop running
