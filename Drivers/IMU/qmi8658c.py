"""

MIT License

Copyright (c) 2023 Ali CHOUCHENE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# qmi8658c.py - IMU library for MicroPython using SPI
# This library is free software; you can redistribute it and/or modify it.

# Import necessary modules
from machine import SPI, Pin
import struct
import time

# General purpose registers
QMI8658_WHO_AM_I = 0x00   # WHO_AM_I register address
QMI8658_REVISION = 0x01   # REVISION register address

# Setup and control registers
QMI8658_CTRL1 = 0x02      # Control register 1 address
QMI8658_CTRL2 = 0x03      # Control register 2 address
QMI8658_CTRL3 = 0x04      # Control register 3 address
QMI8658_CTRL4 = 0x05      # Control register 4 address
QMI8658_CTRL5 = 0x06      # Control register 5 address
QMI8658_CTRL6 = 0x07      # Control register 6 address
QMI8658_CTRL7 = 0x08      # Control register 7 address
QMI8658_CTRL9 = 0x0A      # Control register 9 address

# Data output registers
# Accelerometer
QMI8658_ACC_X_L = 0x35    # Accelerometer X-axis low byte
QMI8658_ACC_X_H = 0x36    # Accelerometer X-axis high byte
QMI8658_ACC_Y_L = 0x37    # Accelerometer Y-axis low byte
QMI8658_ACC_Y_H = 0x38    # Accelerometer Y-axis high byte
QMI8658_ACC_Z_L = 0x39    # Accelerometer Z-axis low byte
QMI8658_ACC_Z_H = 0x3A    # Accelerometer Z-axis high byte

# Gyroscope
QMI8658_GYR_X_L = 0x3B    # Gyroscope X-axis low byte
QMI8658_GYR_X_H = 0x3C    # Gyroscope X-axis high byte
QMI8658_GYR_Y_L = 0x3D    # Gyroscope Y-axis low byte
QMI8658_GYR_Y_H = 0x3E    # Gyroscope Y-axis high byte
QMI8658_GYR_Z_L = 0x3F    # Gyroscope Z-axis low byte
QMI8658_GYR_Z_H = 0x40    # Gyroscope Z-axis high byte

# Temperature sensor
QMI8658_TEMP_L = 0x33     # Temperature sensor low byte
QMI8658_TEMP_H = 0x34     # Temperature sensor high byte

# Soft reset register
QMI8658_RESET = 0x60      # Soft reset register address

# Scale sensitivity values
ACC_SCALE_SENSITIVITY_2G = (1 << 14)  # Sensitivity for ±2g range
ACC_SCALE_SENSITIVITY_4G = (1 << 13)  # Sensitivity for ±4g range
ACC_SCALE_SENSITIVITY_8G = (1 << 12)  # Sensitivity for ±8g range
ACC_SCALE_SENSITIVITY_16G = (1 << 11) # Sensitivity for ±16g range

GYRO_SCALE_SENSITIVITY_16DPS = (1 << 11) # ±16 dps
GYRO_SCALE_SENSITIVITY_32DPS = (1 << 10) # ±32 dps
GYRO_SCALE_SENSITIVITY_64DPS = (1 << 9)  # ±64 dps
GYRO_SCALE_SENSITIVITY_128DPS = (1 << 8) # ±128 dps
GYRO_SCALE_SENSITIVITY_256DPS = (1 << 7) # ±256 dps
GYRO_SCALE_SENSITIVITY_512DPS = (1 << 6) # ±512 dps
GYRO_SCALE_SENSITIVITY_1024DPS = (1 << 5) # ±1024 dps
GYRO_SCALE_SENSITIVITY_2048DPS = (1 << 4) # ±2048 dps

TEMPERATURE_SENSOR_RESOLUTION = (1 << 8) # Temperature sensor resolution (ADC)

# Output data rate (ODR) settings for accelerometer
class AccODR:
    acc_odr_8000 = 0
    acc_odr_4000 = 1
    acc_odr_2000 = 2
    acc_odr_1000 = 3
    acc_odr_500 = 4
    acc_odr_250 = 5
    acc_odr_125 = 6
    acc_odr_62_5 = 7
    acc_odr_31_25 = 8
    acc_odr_128 = 12
    acc_odr_21 = 13
    acc_odr_11 = 14
    acc_odr_3 = 15

# Output data rate (ODR) settings for gyroscope
class GyroODR:
    gyro_odr_8000 = 0
    gyro_odr_4000 = 1
    gyro_odr_2000 = 2
    gyro_odr_1000 = 3
    gyro_odr_500 = 4
    gyro_odr_250 = 5
    gyro_odr_125 = 6
    gyro_odr_62_5 = 7
    gyro_odr_31_25 = 8

# Scale settings for accelerometer
class AccScale:
    acc_scale_2g = 0
    acc_scale_4g = 1
    acc_scale_8g = 2
    acc_scale_16g = 3

# Scale settings for gyroscope
class GyroScale:
    gyro_scale_16dps = 0
    gyro_scale_32dps = 1
    gyro_scale_64dps = 2
    gyro_scale_128dps = 3
    gyro_scale_256dps = 4
    gyro_scale_512dps = 5
    gyro_scale_1024dps = 6
    gyro_scale_2048dps = 7

# Struct for accelerometer axes data
class AccAxes:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

# Struct for gyroscope axes data
class GyroAxes:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

# Struct for data read from QMI8658C
class QmiData:
    def __init__(self):
        self.acc_xyz = AccAxes()
        self.gyro_xyz = GyroAxes()
        self.temperature = 0.0

# Class for QMI8658C IMU
class Qmi8658C:
    def __init__(self, spi: SPI, cs_pin: int):
        self.device_id = None  # Device ID of the QMI8658C
        self.device_revision_id = None  # Revision ID of the QMI8658C
        self.spi = spi  # SPI instance
        self.cs = Pin(cs_pin, Pin.OUT)  # Chip select pin
        self.cs.value(1)  # Deselect device

    def open(self, qmi8658_cfg):
        self.reset()  # Reset the device
        time.sleep(0.1)  # Allow the device to stabilize
        
        # Read WHO_AM_I register
        self.device_id = self.qmi8658_read(QMI8658_WHO_AM_I)
        self.device_revision_id = self.qmi8658_read(QMI8658_REVISION)

        # Configuration would be set here based on the passed configuration
        # For example, setting control registers...

        return True  # Indicate success

    def read(self):
        data = QmiData()

        # Read accelerometer data
        acc_x_l = self.qmi8658_read(QMI8658_ACC_X_L)
        acc_x_h = self.qmi8658_read(QMI8658_ACC_X_H)
        data.acc_xyz.x = struct.unpack('<h', bytes([acc_x_l, acc_x_h]))[0] / ACC_SCALE_SENSITIVITY_2G  # Adjust scaling as needed

        acc_y_l = self.qmi8658_read(QMI8658_ACC_Y_L)
        acc_y_h = self.qmi8658_read(QMI8658_ACC_Y_H)
        data.acc_xyz.y = struct.unpack('<h', bytes([acc_y_l, acc_y_h]))[0] / ACC_SCALE_SENSITIVITY_2G  # Adjust scaling as needed

        acc_z_l = self.qmi8658_read(QMI8658_ACC_Z_L)
        acc_z_h = self.qmi8658_read(QMI8658_ACC_Z_H)
        data.acc_xyz.z = struct.unpack('<h', bytes([acc_z_l, acc_z_h]))[0] / ACC_SCALE_SENSITIVITY_2G  # Adjust scaling as needed

        # Read gyroscope data
        gyro_x_l = self.qmi8658_read(QMI8658_GYR_X_L)
        gyro_x_h = self.qmi8658_read(QMI8658_GYR_X_H)
        data.gyro_xyz.x = struct.unpack('<h', bytes([gyro_x_l, gyro_x_h]))[0] / GYRO_SCALE_SENSITIVITY_16DPS  # Adjust scaling as needed

        gyro_y_l = self.qmi8658_read(QMI8658_GYR_Y_L)
        gyro_y_h = self.qmi8658_read(QMI8658_GYR_Y_H)
        data.gyro_xyz.y = struct.unpack('<h', bytes([gyro_y_l, gyro_y_h]))[0] / GYRO_SCALE_SENSITIVITY_16DPS  # Adjust scaling as needed

        gyro_z_l = self.qmi8658_read(QMI8658_GYR_Z_L)
        gyro_z_h = self.qmi8658_read(QMI8658_GYR_Z_H)
        data.gyro_xyz.z = struct.unpack('<h', bytes([gyro_z_l, gyro_z_h]))[0] / GYRO_SCALE_SENSITIVITY_16DPS  # Adjust scaling as needed

        # Read temperature data
        temp_l = self.qmi8658_read(QMI8658_TEMP_L)
        temp_h = self.qmi8658_read(QMI8658_TEMP_H)
        data.temperature = struct.unpack('<h', bytes([temp_l, temp_h]))[0] / TEMPERATURE_SENSOR_RESOLUTION  # Adjust scaling as needed

        return data

    def reset(self):
        self.qmi8658_write(QMI8658_RESET, 0x01)  # Write soft reset value

    def qmi8658_read(self, reg_address):
        self.cs.value(0)  # Select the device
        self.spi.write(bytearray([reg_address | 0x80]))  # Send read command (MSB set)
        time.sleep(0.01)  # Delay for device response
        data = self.spi.read(1)  # Read 1 byte
        self.cs.value(1)  # Deselect the device
        return data[0]

    def qmi8658_write(self, reg_address, value):
        self.cs.value(0)  # Select the device
        self.spi.write(bytearray([reg_address, value]))  # Send write command
        self.cs.value(1)  # Deselect the device
