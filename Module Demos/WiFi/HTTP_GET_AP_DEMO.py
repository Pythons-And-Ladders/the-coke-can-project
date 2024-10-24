import network
import socket

# Set up Access Point (AP) credentials
SSID = 'The Coke Can Project'      # SSID of the AP
PASSWORD = 'Coke Can'              # Password for the AP
PORT = 80                          # Port number for the web server

def SETUP_ACCESS_POINT(SSID, PASSWORD):
    AP = network.WLAN(network.AP_IF)
    AP.active(True)
    AP.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA2_PSK)

    # Print the IP address of the access point
    print('Access Point IP Address:', AP.ifconfig()[0])
    return AP

def START_WEB_SERVER():
    ADDR = ('0.0.0.0', PORT)  # Bind to all interfaces on port 80
    S = socket.socket()
    S.bind(ADDR)  # Bind the socket to the address
    S.listen(1)
    print('Listening on', ADDR)
    
    return S

# Allow connection from client then receive and decode GET request message
def SERVE_CLIENT(S):
    CL, ADDR = S.accept()
    print('Client connected from', ADDR)
    REQUEST = CL.recv(1024)
    # print('Request:', REQUEST) # Print statement to see the intial request

    # Decode the request
    REQUEST_STR = REQUEST.decode()
    # print("Decoded request:", REQUEST_STR)  # Debug print for the decoded request

    # Parse the request to get the message if it exists
    MESSAGE = None
    if "GET" in REQUEST_STR:
        # Look for the 'msg=' parameter
        MSG_START = REQUEST_STR.find("msg=")
        if MSG_START != -1:
            # Move past 'msg=' to get to the start of the message
            MSG_START += len("msg=")  
            MSG_END = REQUEST_STR.find("&", MSG_START)  # Find the next '&' or end of line
            if MSG_END == -1:  # If no '&' is found, take everything until the end of the line
                MSG_END = REQUEST_STR.find(" ", MSG_START)  # In case no '&', look for space
                if MSG_END == -1:  # If no space, take till the end of the string
                    MSG_END = len(REQUEST_STR)
            MESSAGE = REQUEST_STR[MSG_START:MSG_END]  # Extract the message
            print("Received message:", MESSAGE)

    # Serve a simple HTML page
    RESPONSE = """HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n
                  <html><body><h1>Message received by Access Point!</h1></body></html>\r\n"""
    CL.send(RESPONSE)
    CL.close()

# Deactivate the AP
def SHUTDOWN_ACCESS_POINT(AP):
    print('Shutting down access point...')
    AP.active(False)
    print('Access point shut down.')

def MAIN():
    AP = SETUP_ACCESS_POINT(SSID, PASSWORD)     # Set up the access point
    SERVER_SOCKET = START_WEB_SERVER()          # Start the web server
    
    try:
        SERVE_CLIENT(SERVER_SOCKET)             # Serve a client request
    finally:
        SHUTDOWN_ACCESS_POINT(AP)               # Ensure access point is shut down

# Run the main function
if __name__ == "__main__":
    MAIN()

