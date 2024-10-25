from machine import I2C, Pin
from bme280 import BME280  # BME class from bme280 driver

# Define the I2C pins for Bus 0
SDA = Pin(17)  # SDA pin
SCL = Pin(18)  # SCL pin

# Create I2C interface
I2C_BUS0 = I2C(0, scl=SCL, sda=SDA, freq=400000)

# Setup bme280 sensor
TPH_SENSOR = BME280(I2C_BUS0)

# Read all values from sensor
TPH_SENSOR_DATA = TPH_SENSOR.read_all()

# Format the individual readings to 2 decimal places for readability 
TEMPERATURE = f"{TPH_SENSOR_DATA['temperature']:.1f}" 
PRESSURE = float(f"{TPH_SENSOR_DATA['pressure']:.1f}") * 100 # conversion to Pa from hPa
HUMIDITY = f"{TPH_SENSOR_DATA['humidity']:.1f}"

# Print current temperature, pressure, and humidity readings to the output terminal.
print("Temperature: ", TEMPERATURE)
print("Pressure: ", PRESSURE)
print("Humidity: ", HUMIDITY)
