# PMU Code Overview

This folder contains the demonstration files that exploit the functionality of the onboard power management unit (PMU), the AXP2101.

## Contents:

- `INIT_PMU_DEMO.py`: Code to initialise the PMU and extract the module's chip ID, confirming its connection with the MCU.
- `INTRINSIC_PARAMS_DEMO.py`: Code to extract the battery voltage, system voltage, calculate battery percentage and charging status, and display it on the OLED screen.
- `POWER_I2C_DEMO.py`: Code to power I2C bus with 3.3V, increasing the brightness of text on OLED display.
