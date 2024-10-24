from machine import SPI, Pin
import time
from sx1262 import SX1262

# Pin assignments for SX1262
SPI_BUS = 2
CLK_PIN = Pin(12)
MOSI_PIN = Pin(11)
MISO_PIN = Pin(13)
CS_PIN = Pin(10, Pin.OUT)  # Chip Select
RST_PIN = Pin(5, Pin.OUT)  # Reset
GPIO_PIN = Pin(4, Pin.IN)  # DIO1
IRQ_PIN = Pin(1, Pin.IN)   # IRQ pin

# Create SX1262 LoRa transceiver object
LORA = SX1262(spi_bus=SPI_BUS, clk=CLK_PIN, mosi=MOSI_PIN, miso=MISO_PIN, cs=CS_PIN, irq=IRQ_PIN, rst=RST_PIN, gpio=GPIO_PIN)

# Reset the module
RST_PIN.value(0)  # Set RST low
time.sleep(0.1)  # Wait for 100 ms
RST_PIN.value(1)  # Set RST high
time.sleep(0.5)  # Wait for 500 ms

# Begin communication with SX1262
LORA.begin(freq=868, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

print("Transmitter initialized successfully.")

# Define the unique addresses for the target and source node(s)
TARGET_ADDR = b'\x01'
SOURCE_ADDR = b'\x02'  

while True:
  
    # Create a message with addressing
    MESSAGE = TARGET_ADDR + SOURCE_ADDR + b'testingTXRX'

    # Send the LoRa message
    LORA.send(MESSAGE)
    print("Sent message to node:", TARGET_ADDR, "Message:", message)

    time.sleep(5)  # Wait before sending the next message

