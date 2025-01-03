# Drivers

This folder contains the drivers used within the project at its current state.

## Contents:

- `BME280`: Driver to interact with the onboard BME280 temperature, pressure, and humidity sensor.
- `IMU`: Driver to interact with the onboard QMI8658 inertial measurement unit (IMU).
- `OLED`: Driver to interact with the onboard 1.3" 128x64 SH1106 OLED screen.
- `PMU`: Driver to interact with the onboard AXP2101 power management unit (PMU).
- `MicroSD Card`: Driver to interact with the onboard MicroSD card reader.
- `SX1262`: Driver to interact with the onboard SX1262 LoRa transceiver module.

## Disclaimers:

The IMU and certain functions of the modules listed above have not yet been utilised or tested within the current scope of this project. However, the required drivers for these functionalities are included, though their compatibility and functionality have not been fully verified. 
