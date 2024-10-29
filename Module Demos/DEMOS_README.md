# Module Demos

This folder contains demonstration files showcasing the individual functionality of each onboard module.

## Contents:

- `BLE`: Code to send and receive messages via bluetooth low energy (BLE), using bluetooth and aioble libraries.
- `BME280`: Code to retreive temperature, pressure, and humidity data from the onboard BME280 sensor.
- `GNSS`: Code to retrieve latitude and longtiude data from the onboard Queltec L76K GNSS module.
- `LoRa`: Code to send and receive messages via LoRa (at 868MHz).
- `OLED`: Code to display text onto the SH1106 OLED screen.
- `PMU`: Code to interface with the onboard AXP2101 power management unit (PMU) and retrieve intrinsic node data.
- `RTC`: Code to read date and time from the onboard real-time clock (RTC).
- `WiFi`: Code demonstrating the device's ability to set up an Access Point (AP) for direct connections and host a simple web server, or connect to an existing WiFi network in Station (STA) mode for sending and receiving HTTP GET requests.

## Disclaimer:

The IMU, TF card reader, and certain functions of the modules listed above have not yet been utilised or tested within the current scope of this project. However, the required drivers for these functionalities are included, though their compatibility and functionality have not been fully verified.
