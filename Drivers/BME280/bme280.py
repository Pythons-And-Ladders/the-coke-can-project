"""

Copyright (c) 2015, Kieran Brownlees
All rights reserved unless stated.

Redistribution and use in source and binary forms, with or 
without modification, are permitted provided that the 
following conditions are met:

* Redistributions of source code must retain the above 
copyright notice, this list of conditions and the following 
disclaimer.

* Redistributions in binary form must reproduce the above 
copyright notice, this list of conditions and the following 
disclaimer in the documentation and/or other materials 
provided with the distribution.

* Neither the name of BME280 Python Driver nor the names of its 
contributors may be used to endorse or promote products derived 
from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.

"""

import time
from machine import I2C, Pin

# Define the I2C address for the sensor
BME280_I2CADDR = 0x77  # Default address

class BME280:
    def __init__(self, i2c, address=BME280_I2CADDR):
        self.i2c = i2c
        self.address = address
        self.calibration_h = []
        self.calibration_p = []
        self.calibration_t = []
        self.t_fine = 0.0
        self.setup_run = False

        # Set up the sensor
        self.setup()

    def read_byte_data(self, register):
        """MicroPython-compatible I2C read."""
        return self.i2c.readfrom_mem(self.address, register, 1)[0]

    def write_byte_data(self, register, data):
        """MicroPython-compatible I2C write."""
        self.i2c.writeto_mem(self.address, register, bytes([data]))

    def reset_calibration(self):
        self.calibration_h = []
        self.calibration_p = []
        self.calibration_t = []
        self.t_fine = 0.0

    def populate_calibration_data(self):
        raw_data = []

        for i in range(0x88, 0x88 + 24):
            raw_data.append(self.read_byte_data(i))
        raw_data.append(self.read_byte_data(0xA1))
        for i in range(0xE1, 0xE1 + 7):
            raw_data.append(self.read_byte_data(i))

        self.calibration_t.append((raw_data[1] << 8) | raw_data[0])
        self.calibration_t.append((raw_data[3] << 8) | raw_data[2])
        self.calibration_t.append((raw_data[5] << 8) | raw_data[4])

        self.calibration_p.append((raw_data[7] << 8) | raw_data[6])
        self.calibration_p.append((raw_data[9] << 8) | raw_data[8])
        self.calibration_p.append((raw_data[11] << 8) | raw_data[10])
        self.calibration_p.append((raw_data[13] << 8) | raw_data[12])
        self.calibration_p.append((raw_data[15] << 8) | raw_data[14])
        self.calibration_p.append((raw_data[17] << 8) | raw_data[16])
        self.calibration_p.append((raw_data[19] << 8) | raw_data[18])
        self.calibration_p.append((raw_data[21] << 8) | raw_data[20])
        self.calibration_p.append((raw_data[23] << 8) | raw_data[22])

        self.calibration_h.append(raw_data[24])
        self.calibration_h.append((raw_data[26] << 8) | raw_data[25])
        self.calibration_h.append(raw_data[27])
        self.calibration_h.append((raw_data[28] << 4) | (0x0F & raw_data[29]))
        self.calibration_h.append((raw_data[30] << 4) | ((raw_data[29] >> 4) & 0x0F))
        self.calibration_h.append(raw_data[31])

    def read_adc(self):
        data = []
        for i in range(0xF7, 0xF7 + 8):
            data.append(self.read_byte_data(i))
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw = (data[6] << 8) | data[7]

        return hum_raw, pres_raw, temp_raw

    def read_all(self):
        humidity, pressure, temperature = self.read_adc()
        return {
            "humidity": self.read_humidity(humidity),
            "pressure": self.read_pressure(pressure),
            "temperature": self.read_temperature(temperature)
        }

    def read_humidity(self, hum_raw):
        self.read_temperature()  # Needed to get t_fine
        return self.compensate_humidity(hum_raw)

    def read_pressure(self, pres_raw):
        self.read_temperature()  # Needed to get t_fine
        return self.compensate_pressure(pres_raw)

    def read_temperature(self, temp_raw=None):
        if temp_raw is None:
            _, _, temp_raw = self.read_adc()
        return self.compensate_temperature(temp_raw)

    def compensate_pressure(self, adc_p):
        v1 = (self.t_fine / 2.0) - 64000.0
        v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * self.calibration_p[5]
        v2 += ((v1 * self.calibration_p[4]) * 2.0)
        v2 = (v2 / 4.0) + (self.calibration_p[3] * 65536.0)
        v1 = (((self.calibration_p[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8) + ((self.calibration_p[1] * v1) / 2.0)) / 262144
        v1 = ((32768 + v1) * self.calibration_p[0]) / 32768

        if v1 == 0:
            return 0

        pressure = ((1048576 - adc_p) - (v2 / 4096)) * 3125
        if pressure < 0x80000000:
            pressure = (pressure * 2.0) / v1
        else:
            pressure = (pressure / v1) * 2

        v1 = (self.calibration_p[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
        v2 = ((pressure / 4.0) * self.calibration_p[7]) / 8192.0
        pressure += ((v1 + v2 + self.calibration_p[6]) / 16.0)

        return pressure / 100

    def compensate_temperature(self, adc_t):
        var1 = (adc_t / 16384.0 - self.calibration_t[0] / 1024.0) * self.calibration_t[1]
        var2 = (adc_t / 131072.0 - self.calibration_t[0] / 8192.0) * (adc_t / 131072.0 - self.calibration_t[0] / 8192.0) * self.calibration_t[2]
        self.t_fine = var1 + var2
        temperature = (self.t_fine * 5 + 128) / 256
        return temperature / 100.0

    def compensate_humidity(self, adc_h):
        var_h = self.t_fine - 76800.0
        if var_h == 0:
            return 0

        var_h = (adc_h - (self.calibration_h[3] * 64.0 + self.calibration_h[4] / 16384.0 * var_h)) * (
                self.calibration_h[1] / 65536.0 * (1.0 + self.calibration_h[5] / 67108864.0 * var_h * (
                1.0 + self.calibration_h[2] / 67108864.0 * var_h)))
        var_h *= (1.0 - self.calibration_h[0] * var_h / 524288.0)

        if var_h > 100.0:
            var_h = 100.0
        elif var_h < 0.0:
            var_h = 0.0

        return var_h

    def setup(self):
        """Configure the BME280 sensor settings."""
        if self.setup_run:
            return

        self.write_byte_data(0xF4, 0x00)  # Put the sensor in sleep mode first
        self.write_byte_data(0xF2, 0x01)  # Humidity oversampling x1
        self.write_byte_data(0xF4, 0x27)  # Set mode to normal, pressure & temperature oversampling x1
        self.write_byte_data(0xF5, 0x00)  # Standby time 0.5ms, filter off

        self.populate_calibration_data()  # Populate the calibration data
        self.setup_run = True  # Mark setup as complete
