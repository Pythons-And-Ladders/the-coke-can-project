# WiFi Code Overview

## Access Point (AP) Mode:
- Sets up the device as a WiFi Access Point, allowing other devices to connect directly to it.
- Runs a basic web server on a specified port, capable of accepting and responding to HTTP GET requests.
- Extracts any message parameters sent in the URL (e.g., `msg=<message>`), providing a simple way to receive messages from connected clients.
- The device responds with a confirmation HTML page acknowledging the received message.

## Station (STA) Mode:
- Configures the device to connect to an existing WiFi network (the AP).
- Sends HTTP GET requests to remote servers and listens for responses when connected, allowing it to interact with external web services or APIs.
