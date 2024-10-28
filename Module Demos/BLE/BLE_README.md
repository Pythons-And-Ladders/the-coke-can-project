# BLE Code Overview

This folder contains the demonstration files that exploit the functionality of the integrated Bluetooth and BLE (Bluetooth Low Energy) 

## Contents:

- **BLE_RX_DEMO.py**: This code sets up a BLE server that advertises itself to nearby BLE clients. Upon connection, the server listens for incoming messages from the client, reads the data written to a specified characteristic, and displays it in the shell. The BLE service and characteristic UUIDs are defined within the script, and the program continuously handles client connections and disconnections.
- **BLE_TX_DEMO.py**: This code establishes a BLE client that searches for a specific BLE server named "BLE-Message-Server" (set within `BLE_RX_DEMO.py`) advertising a designated service UUID. Upon locating the server, the client connects, discovers the necessary characteristics for data exchange, and sends a pre-defined message. After confirming the message is sent, the client disconnects cleanly from the server. The code includes handling for scanning, connecting, writing to a characteristic, and disconnecting asynchronously.
