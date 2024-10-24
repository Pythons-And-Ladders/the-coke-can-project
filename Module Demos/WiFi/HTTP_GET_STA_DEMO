import network
import socket
import time

# Define Access Point (AP) credentials
AP_SSID = 'The Coke Can Project'   # SSID of the Access Point (AP)
AP_PASSWORD = 'Coke Can'           # Password for the AP
SERVER_IP = '192.168.4.1'          # IP address of the web server
PORT = 80                          # Port number for the web server

# Setup station (STA) node and try to connect to AP
def SETUP_WIFI(SSID, PASSWORD):
    WLAN = network.WLAN(network.STA_IF)
    WLAN.active(True)
    WLAN.connect(SSID, PASSWORD)
    print('Connecting to Access Point...')
    while not WLAN.isconnected():
        time.sleep(1)
    print('Connected to Access Point!')

    # Print the IP address assigned by the access point
    print('IP Address:', WLAN.ifconfig()[0])
    return WLAN

# Connect to the correct server and port, and send a GET request.
def SEND_HTTP_REQUEST(SERVER_IP, PORT, MESSAGE):
    # Setup and connect to the AP
    S = socket.socket()
    S.connect((SERVER_IP, PORT))

    # Prepare the HTTP GET request with a message as a query parameter
    REQUEST = 'GET /?msg={}&HTTP/1.0\r\nHost: {}\r\n\r\n'.format(MESSAGE, SERVER_IP)

    # Send the request
    S.send(REQUEST.encode())
    print('Request sent:', REQUEST)

    # Receive the response
    RESPONSE = S.recv(1024)
    print('Response from server:', RESPONSE)

    # Close the socket
    S.close()
    
    return RESPONSE

# Decode the resposne recieved from the AP
def DECODE_RESPONSE(RESPONSE):
    RESPONSE_STR = RESPONSE.decode()

    # Separate the headers and body of the HTTP response
    HEADER_END = RESPONSE_STR.find("\r\n\r\n")
    if HEADER_END != -1:
        BODY = RESPONSE_STR[HEADER_END + 4:]  # The body starts after "\r\n\r\n"

        # Find the message within the HTML tags
        START = BODY.find('<h1>')
        END = BODY.find('</h1>')
        if START != -1 and END != -1:
            # Extract and print the message between <h1> and </h1>
            MESSAGE = BODY[START + 4:END]
            print('Response message:', MESSAGE)
        else:
            print("Message not found in response.")
    else:
        print("Malformed HTTP response.")

# Deactivate the station interface
def SHUTDOWN_WIFI(WLAN):
    print('Shutting down Wi-Fi connection...')
    WLAN.active(False)

def MAIN():
    WLAN = SETUP_WIFI(AP_SSID, AP_PASSWORD)                          # Set up Wi-Fi connection
    MESSAGE_TO_SEND = "Hello, Server!"                               # Message to send
    RESPONSE = SEND_HTTP_REQUEST(SERVER_IP, PORT, MESSAGE_TO_SEND)   # Send HTTP request
    DECODE_RESPONSE(RESPONSE)                                        # Decode response from AP
    SHUTDOWN_WIFI(WLAN)                                              # Shut down Wi-Fi connection

# Run the main function
if __name__ == "__main__":
    MAIN()
