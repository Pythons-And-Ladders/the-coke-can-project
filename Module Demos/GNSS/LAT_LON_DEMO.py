import time
from machine import Pin, I2C, UART
from AXP2101 import *
from micropyGPS import MicropyGPS

def INIT_I2C1(SDA_PIN=42, SCL_PIN=41):
    I2C_BUS1 = I2C(1, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
    print("I2C Bus 1 initialised successfully.")
    return I2C_BUS1

def INIT_PMU(I2C_BUS1, ALDO4_VOLTAGE=3300):
    PMU = AXP2101(I2C_BUS1, addr=0x34)  # Replace with actual I2C address if different
    PMU.setALDO4Voltage(ALDO4_VOLTAGE)  # Set the ALDO4 voltage
    PMU.enableALDO4()  # Enable ALDO4
    print("GPS is enabled with voltage: {} mV".format(ALDO4_VOLTAGE))

# Initialise UART for GPS
def INIT_GPS_UART(TX=8, RX=9):
    UART_GPS = UART(1, baudrate=9600, tx=Pin(TX), rx=Pin(RX))
    return UART_GPS

# Read GPS data from the UART
def READ_GPS(UART):
    if UART.any():                        # Check if any data is available data is on the UART
        GPS_DATA = UART.read(UART.any())  # Read available data
        return GPS_DATA                   # Return the GPS data
    return None

# Define main function to parse NMEA sentences and print Lat and Lon data to the shell
def MAIN():
    GPS = MicropyGPS()                  # Initialise GPS object for NMEA sentence parser
    UART_GPS = INIT_GPS_UART()          # Initialise the GPS UART

    while True:
        GPS_DATA = READ_GPS(UART_GPS)                # Read data from GPS
        if GPS_DATA:                                 # Check if any data has been received
            for CHAR in GPS_DATA:                    # Iterate over each character in the received data
                GPS.update(chr(CHAR))                # Update the GPS object with each character

            # Check if valid GPS latitude and longitude values have been received          
            if GPS.latitude and GPS.longitude:       # Validate latitude and longitude
                LATITUDE = GPS.latitude_string()     # Get latitude as a string
                LONGITUDE = GPS.longitude_string()   # Get longitude as a string
                print("Lat: {}".format(LATITUDE))    # Print latitude to the shell
                print("Lon: {}".format(LONGITUDE))   # Print longitude to the shell
            else:
                print("Waiting for fix...")          # Indicate that GPS fix is not been established yet

        time.sleep(1)                                # Delay between reads for stability

# Execute the main function when the script is run directly
if __name__ == "__main__":
    I2C_BUS1 = INIT_I2C1()
    INIT_PMU(I2C_BUS1)
    MAIN()

