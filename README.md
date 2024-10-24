# The Coke Can Project

Welcome to The **Coke Can Project**! This repository provides the tools, code, and guidance to convert the TTGO T-Beam Supreme into a highly configurable, multi-protocol wireless sensor node. The system intelligently classifies and transmits data over **LoRa**, **WiFi**, or **BLE**, depending on Quality of Service (QoS) requirements, urgency, and data importance.

## Why "The Coke Can Project"?

The name "**Coke Can Project**" came from the way the wireless sensor network (WSN) was first conceptualised. In early discussions, we used different soft drink brands to represent the various roles and sensors that each node in the network could have. For example, a **Coke** node could be equipped with environmental sensors, a **Pepsi** node might serve as a router, and a **Fanta** node could act as a gateway or dead letterbox for message storage.

This analogy helped us to easily visualise and distinguish the different functionalities across the network, making it simpler to plan the system’s structure. Additionally, the concept of a "Coke Can" provided a useful reference for the **size and weight** of the nodes, emphasising their portability and versatility. Each node, roughly the size of a standard 330ml can, is compact enough to be deployed in a variety of environments while maintaining flexibility in its role and onboard sensors.

This creative approach simplified the early design process and now reflects the project's adaptability and efficiency in real-world applications.

## Project Overview

The purpose of this project is to design and develop an intelligent data routing system for a WSN. The primary goal is to enhance **energy efficiency**, while ensuring **reliability**, **extensibility** and **flexibility** in data management. This includes both a theoretical design and the physical implementation of a working WSN.

**Key Features**
- **Metadata Management**: Efficient assignment and management of data metadata.
- **Priority Assignment**: Classifies data by urgency and importance to ensure high-priority information is handled first.
- **Traffic Pre-emption**: Optimises network traffic flow by prioritising critical data.
- **Protocol Selection**: Automatically selects the best communication protocol (LoRa, Wi-Fi, or BLE) based on data requirements.
- **Data Transmission**: Secure and reliable data transmission across the WSN.

### System Capabilities
This project turns TTGO T-Beam Supreme Meshtastic devices into customisable wireless sensor nodes capable of environmental monitoring and data classification for transmission using different communication protocols. The system includes the processing of:

- **Intrinsic node data**: e.g., battery percentage and system voltage
- **Extrinsic sensor data**: e.g., temperature, humidity and pressure
- **Network parameters**: e.g., RSSI and transmission error rate

By allowing you to preemptively classify sensor data based on urgency and importance, this system ensures energy-efficient communication and flexible network configurations.

## Product Scope
The project focuses on the development of an intelligent data routing system for various applications, such as disaster management, environmental monitoring, and industrial automation. It provides a flexible, multi-protocol communication system (LoRa, Wi-Fi and BLE) for energy efficient transmission of data.

**In-Scope Tasks:**
- Data collection and labelling
- Priority assignment and pre-emption
- Multi-protocol communication
- System integration and testing

**Out-of-Scope Tasks:**
- Hardware manufacturing
- AI or ML features
- Post-deployment maintenance

### Features
- **Multi-Protocol Communication**: Supports LoRa, WiFi, and BLE.
- **Extensible Framework**: Ability to add your own sensors and modify classification logic.
- **Node Health Monitoring**: Continuously track internal metrics like free memory, battery voltage, and processor load.
- **Environmental Monitoring**: Use a variety of onboard sensors (e.g., BME280) to collect environmental data.
- **Decision Engine**: Automatically prioritise and route data to the appropriate communication channel.

## Getting Started
### Prerequisites
**1. Hardware:**

| General Hardware                    | Specific Model Used                                      |
|-------------------------------------|----------------------------------------------------------|
| TTGO T-Beam Supreme                 | [TTGO T-Beam Supreme (868MHz) Meshtastic with L76K GNSS](https://www.lilygo.cc/products/t-beam-supreme-meshtastic?variant=43067943944373)                            |
| USB to USB-C Data Cable             | [AmazonBasics Data Cable](https://www.amazon.co.uk/Amazon-Basics-Charger-480Mbps-Certified/dp/B01GGKYN0A/ref=sr_1_4?dib=eyJ2IjoiMSJ9.dOHI1-qQuWicZ8t_-pqPinYqxOLlXHpNnYNP2SqEKFvDepBMmupcew3uPBtgRCV7MFRnCYm8TZSSjAFjfFv5S9L-UyBkK8esv-7LWRXeVkPMBFAsTSuuHT2857aqMRdhh6jsVNsQgEkfAw1QlDbFAeAYKJpLdvWp_Vj_mgGagMeRwWnejABYvkvJfCfhCT8TDtSgj4ZqNFCqq4rVHuCdo3qXMf7cADMePZbt2NBYwWanSN-atN2rttrvGqgL-C9L57B64e3myyMMEqHTzyPoydbmiGOErT62FG9YFwRa1Q8.5yiwPH-ljlF_QE15jnZrjKfw6YlOu8MrWCJUrsaJOHQ&dib_tag=se&keywords=USB+to+usb+c+data+cable&nsdOptOutParam=true&qid=1729673117&refinements=p_123%3A234478&rnid=91049098031&s=computers&sr=1-4)                              |
| 2.4GHz Antenna                      | [The PiHut 2.4GHz WiFi/BLE Antenna With U.FL Adapter](https://thepihut.com/products/raspberry-pi-compute-module-4-antenna-kit?variant=39487166185667&currency=GBP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gad_source=1&gclid=Cj0KCQjwveK4BhD4ARIsAKy6pMIKWzKMmUhCy9fwbSfw-WAjaDb6LVd-tD4tyxpErr5FtHXbHRIb2lwaAkapEALw_wcB)  |
| Flat Top 18650 Rechargable Battery  | [Aukido 3.7V 3500mAh NiMH Battery](https://www.amazon.co.uk/Rechargeable-Capacity-Batteries-Headlamp-Flashlight/dp/B0CD2QDDX8) |
| Development Platform (i.e., Laptop) | [HP ProBook 450 G7](https://business.currys.co.uk/catalogue/computing/laptops/windows-laptop/hp-probook-450-g7-15-6-intel-core-i5-10210u-8-gb-ram-256-gb-ssd-uk/P266975P) |

**2. Software:**

| General Software                   | Specific Model Used                                                     |
|------------------------------------|-------------------------------------------------------------------------|
| Thonny IDE (latest stable version) | [thonny-4.1.6.exe for Windows 64-bit (Python 3.0)](https://thonny.org/) |

## Installation and Setup

### 1. Clone the repository:

```bash

git clone https://github.com/Pythons-And-Ladders/the-coke-can-project.git
cd the-coke-can-project

```

### 2. Prepare your Meshtastic device:

These steps will guide you through setting up the TTGO T-Beam Supreme by flashing it with MicroPython. This will replace the Meshtastic firmware, enabling full control over the device for custom configurations.

**2.1. Entering Bootloader Mode:**
- Place the device in bootloader mode by following the [flashing instructions](https://meshtastic.org/docs/hardware/devices/lilygo/tbeam/?t-beam=supreme#flashing) set out by Meshtastic.

**2.2. Connecting the Device**
- Once in bootloader mode, connect the TTGO T-Beam Supreme to your development platform via USB to USB-C data cable.
- Ensure the development platform recognises a device by checking the COM ports: Device Manager > Ports (COM & LPT).

**2.3. Setting Up Thonny IDE**
- Download Thonny IDE and open once download is complete.
- Once opened, click on the bottom right corner of the IDE where it says "Local Python 3 ⋅ Thonny's Python".
- Then from the drop-down menu, click on "Configure Interpreter". This should now have opened the Thonny options window.
- Select the drop-down menu directly under "Which kind of interpreter should Thonny use for running your code?" and select the "MicroPython (ESP32)" option.
- Now within the "Details" box, there should be the hyperlinked text at the bottom right "Install or update MicroPython (esptool) (UF2)". Click this to open the "Install MicroPython (esptool)" window.

**2.4. Flashing MicroPython to the TTGO T-Beam Supreme**
- If not automatically selected when the window opens, click on the "Target port" drop down menu and select the port that corresponds to that of which the TTGO T-BEAM SUPREME is connected to.
- Ensure that the tick box for "Erase all flash before installing (not just the write areas)" is selected before proceeding.
- Now to select the appropriate version of MicroPython for the TTGO T-Beam Supreme, the "ESP32-S3" option should be selected within the "MicroPython family" drop-down menu, and the "Espressif ⋅ ESP32-S3" option within the variant menu.
- From these options, Thonny will automatically assign the most recent version of this MicroPython variant to your device. For reference, the version currently used within this project is 1.23.0.
- Ensure the device is in bootloader mode and press the install button which will erase the meshtastic firmware and flash the native Espressif ESP32-S3 firmware.

**2.5. Final Steps**
Now the TTGO T-Beam Supreme should be ready to run on the microcontroller's native firmware. You can now proceed with configuring it for custom applications, such as turning it into a fully configurable WSN node (of which instructions will follow).

### 3. Install Necessary Files

**3.1. Main WSN Logic Files**
These files are the configurable files that make up the logic behind the wireless sensor network nodes:

- main.py: Main application logic that reads from sensors and node status.
- decision_engine.py: The decision engine responsible for packetising, classifying and selecting the appropriate communication method for the retreived data.

**3.2. Required Drivers**
To interface with the onboard modules of the TTGO T-Beam Supreme, you need to install the necessary drivers. These drivers were pre-configured within the Meshtastic firmware, but since we are now using the ESP32-S3 firmware, you will need to manually reinstall them to ensure proper communication between the board's modules and your development environment. Here is the list of drivers:

- `AXP2101.py`: Driver for the AXP2101 Power Management Unit (PMU).
- `bme280.py`[T]: Driver for the BME280 sensor.
- `sh1106.py`: Driver for the SH1106 OLED screen.
- `sx1262.py`: Driver for the SX1262 LoRa module (must download all sx drivers in order to work).
- `qmi8658c.py`: Driver for the QMI8658 Inertial Measurement Unit (IMU).

> [!NOTE]
> Drivers that can be installed via Thonny (by navigating to Tools > Manage packages... and searching within the micropython-lib and PyPI collections) are marked with a [T]. Installing these files through Thonny is recommended, as it ensures that you are using the most up-to-date versions that are compatible with your MicroPython installation.

**3.3. Required Libraries**
MicroPython comes with several libraries pre-installed, including machine, which provides access to hardware components, and time, which offers a range of functions for handling time-related operations, such as delays and retrieving the current system time. The following libraries are used to help support additional functionalities such as managing I2C communications, handling GPS data, and more:

- `aioble` [T]: A library that enables Bluetooth Low Energy (BLE) operations, facilitating communication with BLE devices.
- `argparse` [T]: A command-line argument parsing library that helps in handling user input parameters when running scripts.
- `asyncio` [T]: A library that provides support for asynchronous programming, allowing for non-blocking code execution.
- `network` [T]: A library used to configure and manage network connections, such as Wi-Fi.
- `sdcard` [T]: A library that facilitates interaction with SD card storage, enabling file reading and writing operations.
- `I2CInterface`: A library designed for communication with I2C devices, simplifying interactions with sensors and other peripherals (required within the AXP2101.py driver).
- `micropyGPS`: A library for parsing GPS NMEA sentences, making it easy to extract location information from GPS modules.

> [!NOTE]
> Drivers that can be installed via Thonny (by navigating to Tools > Manage packages... and searching within the micropython-lib and PyPI collections) are marked with a [T]. Installing these files through Thonny is recommended, as it ensures that you are using the most up-to-date versions that are compatible with your MicroPython installation.

### 4. Upload Necessary Files to Device
After downloading all the necessary files to your development platform's local directory, launch Thonny and navigate to the files tab on the left side of the window. Here, you should see all the downloaded files listed. Select all the files, right-click to open the actions menu, and choose "Upload to /". While the files upload to your device, feel free to grab a coffee or a cup of tea (it may take a few minutes). Once the upload is complete, you will find the files in the "MicroPython device" tab below the files section on the left side of the window, accompanied by the "boot.py" file.

## Basic Usage
Once the TTGO T-Beam Supreme has been setup, and all files successfuly uploaded to the device, you can begin to exploit its functional capacity.

It is recommended that you go through the `Module Demos` folder to ensure the device has been configured correctly in a module-by-module manner. This will enable you to ensure each component on the board operates as expected and gain familiarity with the individual pieces of code that the `main.py` and `decision_engine.py` files are comprised of.

Once this has been conducted, configure the `decision_engine.py` file by modifying the thresholds and measured parameters to suit your application's needs and run the `main.py` file.

The main.py file will execute, collecting sensor data, classifying it based on urgency and importance, and transmitting it via LoRa, WiFi, or BLE.

Synthetic Data Handling: If you want to simulate multimedia data (e.g., video or audio), modify the data_type in the packetisation function to handle synthetic sensor inputs.

## Extending the Project
The current project offers several opportunities for expansion. While the IMU is not yet interfaced due to challenges with configuring its control registers, this could be explored for advanced motion sensing in future updates. Additionally, the GPIO pins, though unused for now, provide the flexibility to add more sensors as needed. SD card functionality could also be improved, as only certain formats (SD/SDHC with FAT32) are compatible, and further refinement could ensure smoother data storage.

Additional expansions include customising the decision engine to modify how data is classified and prioritised, adding network failover logic to guarantee message delivery through the best available communication protocol, and further optimising overall system performance.

These enhancements would build on the project's solid foundation without detracting from its current functionality.

## File Structure
`main.py`: Main application file that handles sensor data collection and transmission.
`decision_engine.py`: Handles the decision-making process for classifying sensor data and selecting communication protocols.
`Drivers`: A folder containing all of the necessary drivers specified above.
`Libraries`: A folder containing all of the necessary libraries specified above.
`Module Demos`: A folder containing demo files that exploit the functionality of the individual modules on the board, such as the LoRa transceiver, OLED screen, PMU, etc.

## Roadmap
[FILL IN]

## Contributing
Contributions to improve the project and expand its functionality are more than welcome. Feel free to:
- Submit bug reports and feature requests in the Issues section.
- Fork the repository, make your changes, and submit a pull request.

## License
[FILL IN]
