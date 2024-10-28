# WiFi Code Overview

This folder contains demonstration files showcasing the WiFi capabilities of the onboard ESP32-S3 microcontroller (MCU).

## Contents:

- **`HTTP_GET_AP_DEMO.py`**: This code demonstrates how to configure the device in Access Point (AP) mode, allowing other devices to connect directly to it. It runs a simple web server on a specified port, where it can accept and respond to HTTP GET requests. Additionally, it can extract any message parameters sent in the URL (e.g., `msg=<message>`), providing a straightforward method to receive messages from connected clients. The device acknowledges each received message by responding with a confirmation HTML page (acknowledgement response).
- **`HTTP_GET_STA_DEMO.py`**: This code demonstrates how to configure the device in Station (STA) mode, enabling it to connect to an existing WiFi network (in this case the AP). Once connected, the device can send HTTP GET requests to remote servers and process the responses, allowing it to interact with external web services or APIs.
