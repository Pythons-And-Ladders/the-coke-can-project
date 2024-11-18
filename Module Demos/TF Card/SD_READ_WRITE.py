from machine import SPI, Pin
import os
from sdcard import SDCard

def SD_READ_WRITE_TEST():
    # Initialise SPI with the correct pins
    SPI = SPI(1, baudrate=4000000, polarity=0, phase=0, sck=Pin(36), mosi=Pin(35), miso=Pin(37))
    # Chip Select pin
    CS = Pin(47, Pin.OUT)  
    
    # Create SD card object
    SD = SDCard(SPI, CS)
    
    # Try to mount the SD card and handle errors
    try:
        # Deactivate and then activate the SD card chip select
        # Deactivate SD card
        CS.value(1) 
        # Activate SD card
        CS.value(0) 

        # Create a FAT filesystem
        VFS = os.VfsFat(sd)

        # Mount the filesystem
        os.mount(VFS, "/fc")
        print("Filesystem mounted successfully")
        # List all files on the SD card
        print("SD Card files:", os.listdir("/fc"))

        # Write file to the MicroSD card's file system
        FILENAME = "/fc/test.txt"
        with open(FILENAME, "w") as F:
            WRITTEN_CONTENT = "Test Data - Testing write functionality"
            F.write(WRITTEN_CONTENT)
        print("File written with:", WRITTEN_CONTENT)

        # Read from the file in the MicroSD card's file system
        with open(FILENAME, "r") as F:
            READ_CONTENT = F.read()
        print("Read from file:", READ_CONTENT)
        if READ_CONTENT == WRITTEN_CONTENT:
            print("File content read successfully:")

    except OSError as e:
        print("Error: SD card not detected or initialisation failed.")
        print("Error details:", e)

# Run the sd card write and read test function
SDTEST()

