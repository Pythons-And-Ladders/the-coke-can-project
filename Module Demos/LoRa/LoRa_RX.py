from machine import Pin
import time
from sx1262 import SX1262

# Pin assignments for SX1262
SPI_BUS = 2                # SPI bus
CLK_PIN = Pin(12)          # SCLK pin
MOSI_PIN = Pin(11)         # MOSI pin
MISO_PIN = Pin(13)         # MISO pin
CS_PIN = Pin(10, Pin.OUT)  # Chip Select
RST_PIN = Pin(5, Pin.OUT)  # Reset
GPIO_PIN = Pin(4, Pin.IN)  # DIO1
IRQ_PIN = Pin(1, Pin.IN)   # IRQ pin

# Create SX1262 LoRa transceiver object
LORA = SX1262(spi_bus=SPI_BUS, clk=CLK_PIN, mosi=MOSI_PIN, miso=MISO_PIN, cs=CS_PIN, irq=IRQ_PIN, rst=RST_PIN, gpio=GPIO_PIN)

# Reset the module
RST_PIN.value(0)  # Set RST low
time.sleep(0.1)   # Wait for 100 ms
RST_PIN.value(1)  # Set RST high
time.sleep(0.5)   # Wait for 500 ms

# Begin communication with SX1262
LORA.begin(freq=868, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

print("Receiver initialized successfully.")

# Define the unique addresses for the target and source node(s)
TARGET_ADDR = b'\x01'
SOURCE_ADDR = b'\x02'  

# Function to handle received messages
def cb(EVENTS):
    if EVENTS & SX1262.RX_DONE:
        MESSAGE, ERR = LORA.recv()
        ERROR = SX1262.STATUS[ERR]
        if ERROR == 'ERR_NONE':
            # Extract the destination and source addresses
            TARGET = MESSAGE[0:1]  # First byte is the destination address
            SOURCE = MESSAGE[1:2]  # Second byte is the source address
            PAYLOAD = MESSAGE[2:]  # The rest of the message is the actual payload

            # Check if the message is for this node and from the expected source
            if TARGET == TARGET_ADDR and SOURCE == SOURCE_ADDR:
                print('Received message from source', SOURCE, ':', PAYLOAD)
            else:
                print('Message not for this node or from unexpected source. Ignored.')

        else:
            print('Received message with error:', ERROR)
        print('Received message:', MESSAGE, 'with status:', ERROR)

# Set callback for receiving messages
LORA.setBlockingCallback(False, cb)  # Use non-blocking callback

while True:
    time.sleep(1)  # Keep the loop running
