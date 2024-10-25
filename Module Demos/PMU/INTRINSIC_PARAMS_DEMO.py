from AXP2101 import *
import time
from machine import Pin, I2C
from sh1106 import SH1106_I2C

# Define I2C Pins and Addresses
OLED_SCL_PIN = 18
OLED_SDA_PIN = 17
PMU_SCL_PIN = 41
PMU_SDA_PIN = 42
PMU_ADDR = AXP2101_SLAVE_ADDRESS

# Initialise the OLED I2C bus and OLED display
def INIT_OLED():
    I2C_BUS0 = I2C(0, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN))
    OLED = SH1106_I2C(128, 64, I2C_BUS0)
    return OLED

# Initialise the I2C bus for PMU
def INIT_PMU_I2C():
    I2C_BUS1 = I2C(1, scl=Pin(PMU_SCL_PIN), sda=Pin(PMU_SDA_PIN))
    return AXP2101(I2C_BUS1, addr=PMU_ADDR)

# Convert millivolts to volts
def MV_TO_V(MV):
    return MV / 1000

# Convert voltage to battery percentage
def VOLTAGE_TO_PERCENTAGE(VOLTAGE):
    VOLTAGE_PERCENT_MAP = [
        (4.20, 100), (3.60, 0)
    ]
    if VOLTAGE >= 4.20:
        return 100
    elif VOLTAGE <= 3.56:
        return 0
    for i in range(len(VOLTAGE_PERCENT_MAP) - 1):
        V_HIGH, P_HIGH = VOLTAGE_PERCENT_MAP[i]
        V_LOW, P_LOW = VOLTAGE_PERCENT_MAP[i + 1]
        if V_LOW <= VOLTAGE <= V_HIGH:
            PERCENTAGE = P_LOW + (P_HIGH - P_LOW) * ((VOLTAGE - V_LOW) / (V_HIGH - V_LOW))
            return round(PERCENTAGE)
    return 0

# Display intrinsic system metrics on OLED
def DISPLAY_SYSTEM_METRICS(PMU, OLED):
    # Retrieve battery and system parameters from PMU
    BATT_VOLTAGE = MV_TO_V(PMU.getBattVoltage())
    SYS_VOLTAGE = MV_TO_V(PMU.getSystemVoltage())
    BATT_PERCENTAGE = VOLTAGE_TO_PERCENTAGE(BATT_VOLTAGE)
    # Display the parameters onto the OLED screen
    OLED.fill(0)
    OLED.text("Battery: {:.2f} V".format(BATT_VOLTAGE), 0, 0)
    OLED.text("System: {:.2f} V".format(SYS_VOLTAGE), 0, 10)
    OLED.text("Battery%: {}%".format(BATT_PERCENTAGE), 0, 20)
    OLED.text("Charging: {}".format("Yes" if PMU.isCharging() else "No"), 0, 30)
    OLED.text("Discharging: {}".format("Yes" if PMU.isDischarge() else "No"), 0, 40)
    OLED.text("Standby: {}".format("Yes" if PMU.isStandby() else "No"), 0, 50)
    OLED.show()

# Main function to initialise I2C buses, OLED screen and PMU. Display metrics to OLED screen.
def MAIN():
    OLED = INIT_OLED()
    PMU = INIT_PMU_I2C()
    if PMU.getChipID() != XPOWERS_AXP2101_CHIP_ID:
        print("PMU is not online...")
        return

    print('PMU initialized, Chip ID: {}'.format(hex(PMU.getChipID())))

    # Continuous loop with exception handling for clean exit
    try:
        while True:
            DISPLAY_SYSTEM_METRICS(PMU, OLED)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Program interrupted by user, exiting...")
    finally:
        # Clear screen on exit
        OLED.fill(0)
        OLED.show()
        print("Exited cleanly.")

if __name__ == "__main__":
    MAIN()
