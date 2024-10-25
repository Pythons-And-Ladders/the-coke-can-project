from machine import I2C, Pin

# Define I2C pins and AXP2101 address
SCL_PIN = 41            # SCL pin
SDA_PIN = 42            # SDA pin
AXP2101_ADDR = 0x34     # PMU address

# Register Definitions
_AXP2101_LDO_ONOFF_CTRL0 = 0x90    # Register to enable linear dropout (LDO) voltage regulator
_AXP2101_LDO_VOL0_CTRL = 0x92      # Register to set LDO voltage
_AXP2101_LDO1_VOL_MIN = 500        # Minimum voltage in mV
_AXP2101_LDO1_VOL_STEPS = 100      # Step size in mV

# Initialize I2C communication
I2C_BUS = I2C(1, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))

def ENABLE_LDO_FOR_I2C(VOLTAGE_MV):
    # Clamp voltage to minimum to ensure module does not receive too much voltage
    VOLTAGE_MV = max(VOLTAGE_MV, _AXP2101_LDO1_VOL_MIN)
    
    # Calculate the number of steps needed to set the desired voltage
    STEPS = (VOLTAGE_MV - _AXP2101_LDO1_VOL_MIN) // _AXP2101_LDO1_VOL_STEPS
    print(f"Setting LDO voltage to {VOLTAGE_MV} mV (Steps: {STEPS})")

    # Set the LDO voltage and enable it
    I2C_BUS.writeto_mem(AXP2101_ADDR, _AXP2101_LDO_VOL0_CTRL, bytes([STEPS]))
    I2C_BUS.writeto_mem(AXP2101_ADDR, _AXP2101_LDO_ONOFF_CTRL0, bytes([0x01]))  # Enable LDO0
    print("LDO for I2C enabled.")

# Enable the LDO powering I2C bus with a voltage of 3300 mV
ENABLE_LDO_FOR_I2C(3300)
