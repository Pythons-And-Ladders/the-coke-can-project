from machine import RTC
import time

# Initialise real time clock (RTC)
RTC = RTC()

# Set an infinite loop to tell the time every second
while True:

    # Extract the date and time data from the RTC
    TIME = RTC.datetime()

    # Structure the time and date into a readable format 
    time_string = "Time: {:02}:{:02}:{:02}".format(TIME[4], TIME[5], TIME[6])
    date_string = "Date: {:02}/{:02}/{:02}".format(TIME[2], TIME[1], TIME[0])

    # Output the formatted date and time
    print(date_string, time_string)
    
    time.sleep(1)
