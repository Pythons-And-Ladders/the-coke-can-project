import time
from machine import I2C, Pin, UART
from decision_engine import Packetisation, DecisionEngine
from bme280 import BME280
from sh1106 import SH1106_I2C
from AXP2101 import *
from micropyGPS import MicropyGPS
import json
from sx1262 import SX1262
import asyncio
import aioble
import bluetooth
import network
import socket

# GPS packet every 2 minutes
GPS_INTERVAL = 30  
# BME280 packet every minute
BME_INTERVAL = 20   
# PMU packet every 30 seconds
PMU_INTERVAL = 10   

# Example sensor ID
SENSOR_ID = 1  

# Constants
# SDA pin for I2C1 (OLED)
SDA_PIN1 = 17
# SCL pin for I2C1 (OLED)
SCL_PIN1 = 18  

# SDA pin for I2C2 (AXP2101)
SDA_PIN2 = 42
# SCL pin for I2C2 (AXP2101)
SCL_PIN2 = 41  

# Initialise I2C interfaces
# For OLED
i2c1 = I2C(0, scl=Pin(SCL_PIN1), sda=Pin(SDA_PIN1), freq=400000)
# For AXP2101
i2c2 = I2C(1, scl=Pin(SCL_PIN2), sda=Pin(SDA_PIN2))  

# Initialise OLED display
oled = SH1106_I2C(128, 64, i2c1)

# Initialise BME280 sensor
bme280 = BME280(i2c1)

# Initialise AXP2101 Power Management Unit
PMU = AXP2101(i2c2, addr=AXP2101_SLAVE_ADDRESS)
ALDO4_VOLTAGE = 3300  # Set ALDO4 to 3.3V
PMU.setALDO4Voltage(ALDO4_VOLTAGE)
PMU.enableALDO4()
print("ALDO4 is enabled with voltage: {} mV".format(ALDO4_VOLTAGE))

# UUIDs for the BLE service and characteristic
_MESSAGE_SERVICE_UUID = bluetooth.UUID(0x1234)
_MESSAGE_CHARACTERISTIC_UUID = bluetooth.UUID(0x1235)

# Configuration for Wi-Fi access point
AP_SSID = 'CokeCanProject'  # Password for the access point
AP_PASSWORD = 'CokeCanPassword'
SERVER_IP = '192.168.4.1'  # IP address of the web server (access point)
PORT = 80  # Port number for the web server

# Initialise I2C for OLED
sda = Pin(17)  # SDA pin
scl = Pin(18)  # SCL pin
i2c = I2C(0, scl=scl, sda=sda, freq=400000)
oled = SH1106_I2C(128, 64, i2c)
oled.fill(0)  # Clear the display at startup
oled.show()

# Pin assignments for SX1262
cs_pin = Pin(10, Pin.OUT)  # Chip Select
rst_pin = Pin(5, Pin.OUT)  # Reset
gpio_pin = Pin(4, Pin.IN)  # DIO1
irq_pin = Pin(1, Pin.IN)   # IRQ pin

# Create SX1262 object
sx = SX1262(spi_bus=2, clk=12, mosi=11, miso=13, cs=cs_pin, irq=irq_pin, rst=rst_pin, gpio=gpio_pin)

# Reset the module
def reset_sx1262():
    """Reset the SX1262 module."""
    rst_pin.value(0)  # Set RST low
    time.sleep(0.1)  # Wait for 100 ms
    rst_pin.value(1)  # Set RST high
    time.sleep(0.5)  # Wait for 500 ms

reset_sx1262()

# Begin communication with SX1262
def initialise_lora():
    """Initialise LoRa communication parameters."""
    sx.begin(freq=868, bw=500.0, sf=12, cr=8, syncWord=0x12,
             power=-5, currentLimit=60.0, preambleLength=8,
             implicit=False, implicitLen=0xFF,
             crcOn=True, txIq=False, rxIq=False,
             tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

initialise_lora()

class MessageClient:
    def __init__(self, device):
        self._device = device
        self._connection = None
        self._message_characteristic = None

    async def connect(self):
        print(f"Connecting to {self._device}...")
        try:
            self._connection = await self._device.connect()
            if not self._connection:
                print("Failed to connect to the device.")
                return
            
            print("Connected successfully. Discovering services...")
            message_service = await self._connection.service(_MESSAGE_SERVICE_UUID)

            if not message_service:
                print(f"Service with UUID {_MESSAGE_SERVICE_UUID} not found!")
                return
            
            print("Service found, discovering characteristic...")
            self._message_characteristic = await message_service.characteristic(_MESSAGE_CHARACTERISTIC_UUID)

            if not self._message_characteristic:
                print(f"Characteristic with UUID {_MESSAGE_CHARACTERISTIC_UUID} not found!")
                return

            print("Characteristic found, ready to send messages.")

        except Exception as e:
            print(f"Error during connection or service discovery: {e}")

    async def send_message(self, message):
        if self._message_characteristic:
            print("Sending message to BLE characteristic...")
            await self._message_characteristic.write(message)
            print("Message sent:", message)

            # Optional: Add a delay to allow processing
            await asyncio.sleep(0.1)

            # Read back to confirm the message was written correctly
            read_message = await self._message_characteristic.read()
            print(f"Confirmed read from characteristic: {read_message}")
        else:
            print("Message characteristic is not available!")

    async def disconnect(self):
        if self._connection:
            await self._connection.disconnect()
            print("Disconnected from BLE device.")

def setup_wifi(ssid, password):
    """Set up the Wi-Fi station interface and connect to the access point."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print('Connecting to Access Point...')
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to Access Point!')

    print('IP Address:', wlan.ifconfig()[0])
    return wlan

def send_http_request(server_ip, port, message):
    """Send an HTTP GET request with a message and RSSI value."""
    s = socket.socket()
    try:
        # Prepare message with RSSI value
        request = f'GET /?msg={message.decode()}&HTTP/1.0\r\nHost: {server_ip}\r\n\r\n'
        s.connect((server_ip, port))
        s.send(request.encode())
        print('Request sent:', request)

        # Receive the response
        response = s.recv(1024)
        print('Response from server:', response)
    except Exception as e:
        print(f"Error during HTTP request: {e}")
    finally:
        s.close()  # Ensure the socket is closed

def shutdown_wifi(wlan):
    """Shut down the Wi-Fi connection."""
    print('Shutting down Wi-Fi connection...')
    wlan.active(False)  # Deactivate the station interface

def display_received_message(msg):
    """Display the received message on the OLED."""
    oled.fill(0)
    oled.text("Message received:", 0, 0)
    oled.text(f"{msg.decode()}", 0, 20)
    oled.show()  # Ensure the display is updated

def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        if err:
            print(f"Error receiving message: {SX1262.STATUS[err]}")
            return
        print('Received message:', msg)
        display_received_message(msg)

def mV_to_V(mv):
    return mv / 1000

def voltage_to_percentage(voltage):
    """
    Converts battery voltage to an estimated percentage.
    """
    # Voltage to percentage approximation table
    voltage_percent_map = [
        (4.20, 100),
        (4.19, 99),
        (4.18, 98),
        (4.17, 97),
        (4.16, 96),
        (4.15, 95),
        (4.14, 94),
        (4.13, 93),
        (4.12, 92),
        (4.11, 91),
        (4.10, 90),
        (4.09, 89),
        (4.08, 88),
        (4.07, 87),
        (4.06, 86),
        (4.05, 85),
        (4.04, 84),
        (4.03, 83),
        (4.02, 82),
        (4.01, 81),
        (4.00, 80),
        (3.99, 79),
        (3.98, 78),
        (3.97, 77),
        (3.96, 76),
        (3.95, 75),
        (3.94, 74),
        (3.93, 73),
        (3.92, 72),
        (3.91, 71),
        (3.90, 70),
        (3.89, 68),
        (3.88, 66),
        (3.87, 64),
        (3.86, 62),
        (3.85, 60),
        (3.84, 58),
        (3.83, 56),
        (3.82, 54),
        (3.81, 52),
        (3.80, 50),
        (3.79, 48),
        (3.78, 46),
        (3.77, 44),
        (3.76, 42),
        (3.75, 40),
        (3.74, 38),
        (3.73, 36),
        (3.72, 34),
        (3.71, 32),
        (3.70, 30),
        (3.69, 27),
        (3.68, 24),
        (3.67, 22),
        (3.66, 19),
        (3.65, 17),
        (3.64, 15),
        (3.63, 13),
        (3.62, 11),
        (3.61, 9),
        (3.60, 7),
        (3.59, 5),
        (3.58, 3),
        (3.57, 1),
        (3.56, 0)
    ]
    
    # If voltage is greater than 4.2V, cap at 100%
    if voltage >= 4.20:
        return 100
    # If voltage is lower than 3.56V, cap at 0%
    elif voltage <= 3.56:
        return 0

    # Find the corresponding percentage by checking where the voltage falls in the table
    for i in range(len(voltage_percent_map) - 1):
        v_high, p_high = voltage_percent_map[i]
        v_low, p_low = voltage_percent_map[i + 1]
        
        if v_low <= voltage <= v_high:
            # Linear interpolation between the two points
            percentage = p_low + (p_high - p_low) * ((voltage - v_low) / (v_high - v_low))
            return round(percentage)
    
    # In case the voltage doesn't match (should not happen with the provided range)
    return 0

# Function to initialise GPS and handle data reading
def INIT_GPS():
    # GPS on UART1
    GPS_UART = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))  
    # Initialise MicropyGPS instance
    GPS = MicropyGPS()  
    print("GPS module initialised.")
    return GPS_UART, GPS

# Function to read GPS data
def read_gps(uart):
    if uart.any():
        # Read available GPS data
        gps_data = uart.read(uart.any())  
        return gps_data
    return None

# Function to update GPS and process data
def UPDATE_GPS(GPS_UART, GPS):
    gps_data = read_gps(GPS_UART)
    if gps_data:
        for char in gps_data:
            # Update GPS object with incoming data
            GPS.update(chr(char))
        return True
    return False

# Function to get GPS data with non-sero check and display on OLED
def GET_GPS_DATA(GPS):
    if GPS.latitude[0] != 0 and GPS.longitude[0] != 0:
        latitude = GPS.latitude_string().replace('°', ' deg ')
        longitude = GPS.longitude_string().replace('°', ' deg ')
        fix_status = "Fix: Valid"
    else:
        latitude = "Waiting for fix..."
        longitude = ""
        fix_status = "Fix: None"

    # Display on OLED
    oled.fill(0)
    oled.text(fix_status, 0, 0)
    oled.text(f"Lat: {latitude}", 0, 10)
    oled.text(f"Lon: {longitude}", 0, 20)
    oled.show()

    return fix_status, latitude, longitude

def create_and_print_bme_packets(bme280_data, engine):
    temperature_payload = json.dumps(bme280_data['temperature']).encode()
    pressure_payload = json.dumps(bme280_data['pressure']).encode()
    humidity_payload = json.dumps(bme280_data['humidity']).encode()
    temperature_packet = Packetisation(sensor_id='BME', sensor_data={'temperature': bme280_data['temperature']}, data_type='temperature', decision_engine=engine, payload=temperature_payload, qos=1)
    pressure_packet = Packetisation(sensor_id='BME', sensor_data={'pressure': bme280_data['pressure']}, data_type='pressure', decision_engine=engine, payload=pressure_payload, qos=1)
    humidity_packet = Packetisation(sensor_id='BME', sensor_data={'humidity': bme280_data['humidity']}, data_type='humidity', decision_engine=engine, payload=humidity_payload, qos=1)
    print(temperature_packet.get_packet())
    print(f"QoS: {temperature_packet.packet['header']['qos']}, Radio: {temperature_packet.packet['header']['radio']}")
    print(pressure_packet.get_packet())
    print(f"QoS: {pressure_packet.packet['header']['qos']}, Radio: {pressure_packet.packet['header']['radio']}")
    print(humidity_packet.get_packet())
    print(f"QoS: {humidity_packet.packet['header']['qos']}, Radio: {humidity_packet.packet['header']['radio']}")

    return temperature_packet, pressure_packet, humidity_packet

def create_and_print_pmu_packets(pmu_data, engine):
    batt_level_payload = json.dumps(pmu_data['battery_level']).encode()
    sys_voltage_payload = json.dumps(pmu_data['system_voltage']).encode()
    batt_level_packet = Packetisation(sensor_id='PMU', sensor_data={'battery_level': pmu_data['battery_level']}, data_type='battery_level', decision_engine=engine, payload=batt_level_payload, qos=2)
    sys_voltage_packet = Packetisation(sensor_id='PMU', sensor_data={'system_voltage': pmu_data['system_voltage']}, data_type='system_voltage', decision_engine=engine, payload=sys_voltage_payload, qos=2)
    print(batt_level_packet.get_packet())
    print(f"QoS: {batt_level_packet.packet['header']['qos']}, Radio: {batt_level_packet.packet['header']['radio']}")
    print(sys_voltage_packet.get_packet())
    print(f"QoS: {sys_voltage_packet.packet['header']['qos']}, Radio: {sys_voltage_packet.packet['header']['radio']}")
    
    return batt_level_packet, sys_voltage_packet

def send_wifi_data(packet):
    """Send data packet over Wi-Fi (HTTP request)."""
    # Use the data in the packet (e.g., payload or message) for the request
    message = packet['payload']  # Assuming the packet contains a 'payload' field
    send_http_request(SERVER_IP, PORT, message)

def send_ble_data(packet):
    """Send data packet over Bluetooth Low Energy (BLE)."""
    message = packet['payload']
    # Example of BLE device setup, assuming `message_client` is instantiated
    message_client = MessageClient(device=device)  # Replace with actual device
    asyncio.run(message_client.connect())
    asyncio.run(message_client.send_message(message))
    asyncio.run(message_client.disconnect())

def send_lora_data(packet):
    """Send data packet over LoRa."""
    message = packet['payload']
    sx.setBlockingCallback(False, cb)
    sx.send(message)
    print(f"Sent message over LoRa: {message}")

def send_data(packet):
    """Function to send data based on the packet's radio type."""
    packet = packet.get_packet()
    radio_type = packet['header']['radio']
    
    if radio_type == "WiFi/LoRa - range dependent":
        # if packet['header']['distance/rssi'] >= distance_threshold:
            # send_lora_data(packet)
        # else:
        #send_wifi_data(packet)
        send_lora_data(packet)
    elif radio_type == "WiFi":
        #send_wifi_data(packet)
        send_lora_data(packet)
    elif radio_type == "LoRa":
        send_lora_data(packet)
    elif radio_type == "BLE":
        #send_ble_data(packet)
        send_lora_data(packet)
    else:
        print(f"Unknown radio type: {radio_type}. Data not sent.")

def handle_gps_data(last_gps_time, GPS_UART, GPS, engine, oled):
    current_time = time.time()
    if current_time - last_gps_time >= GPS_INTERVAL:
        gps_available = UPDATE_GPS(GPS_UART, GPS)
        if gps_available:
            FIX_STATUS, LATITUDE, LONGITUDE = GET_GPS_DATA(GPS)
            if FIX_STATUS == "Fix: Valid":
                gps_data = {
                    'latitude': LATITUDE,
                    'longitude': LONGITUDE
                }
                gps_payload = json.dumps(gps_data).encode()
                gps_packet = Packetisation(sensor_id='GPS', sensor_data=gps_data, data_type='gps', decision_engine=engine, payload=gps_payload, qos=3)
                # urgency, priority, traffic_type, qos, radio = engine.classify_data(gps_data, 'gps')
                print(gps_packet.get_packet())
                print(f"QoS: {gps_packet.packet['header']['qos']}, Radio: {gps_packet.packet['header']['radio']}")
                oled.fill(0)
                oled.text("GPS packet created", 0, 0)
                oled.show()
                return current_time, gps_packet
        return current_time, None  # No GPS data available, return None
    return last_gps_time, None  # No new GPS data, return last time and None

def handle_bme_data(last_bme_time, bme280, engine, oled):
    current_time = time.time()
    if current_time - last_bme_time >= BME_INTERVAL:
        sensor_data = bme280.read_all()
        bme280_data = {
            'temperature': float(f"{sensor_data['temperature']:.1f}"),
            'pressure': float(f"{sensor_data['pressure'] * 100:.2f}"),
            'humidity': float(f"{sensor_data['humidity']:.1f}")
        }
        temperature_packet, pressure_packet, humidity_packet = create_and_print_bme_packets(bme280_data, engine)
        oled.fill(0)
        oled.text("BME packet created", 0, 10)
        oled.show()
        return current_time, temperature_packet, pressure_packet, humidity_packet
    return last_bme_time, None, None, None  # No new BME data

def handle_pmu_data(last_pmu_time, PMU, engine, oled):
    current_time = time.time()
    if current_time - last_pmu_time >= PMU_INTERVAL:
        batt_voltage = PMU.getBattVoltage()
        sys_voltage = PMU.getSystemVoltage()
        pmu_data = {
            'battery_level': float(voltage_to_percentage(mV_to_V(batt_voltage))),
            'system_voltage': mV_to_V(sys_voltage)
        }
        batt_level_packet, sys_voltage_packet = create_and_print_pmu_packets(pmu_data, engine)
        oled.fill(0)
        oled.text("PMU packet created", 0, 20)
        oled.show()
        return current_time, batt_level_packet, sys_voltage_packet
    return last_pmu_time, None, None  # No new PMU data

async def main():
    # Initialise GPS
    GPS_UART, GPS = INIT_GPS()
    
    # Setup Wi-Fi connection
    wlan = setup_wifi(AP_SSID, AP_PASSWORD)

    # Start BLE scanning for the specific device
    async with aioble.scan(5000, 30000, 30000, active=True) as scanner:
        async for result in scanner:
            if result.name() == "BLE-Message-Server" and _MESSAGE_SERVICE_UUID in result.services():
                device = result.device
                break
        else:
            print("BLE server not found.")
            shutdown_wifi(wlan)
            return

    # Connect to the BLE device
    client = MessageClient(device)
    await client.connect()

    # Ensure the client is connected and ready
    if not client._message_characteristic:
        print("Failed to connect to BLE service.")
        shutdown_wifi(wlan)
        return

    # Initialise decision engine
    engine = DecisionEngine()

    # Variables to track the last time each packet was created
    last_gps_time = time.time()
    last_bme_time = time.time()
    last_pmu_time = time.time()

    while True:
        # Call sensor handlers and update last_*_time variables
        last_gps_time, gps_packet = handle_gps_data(last_gps_time, GPS_UART, GPS, engine, oled)
        last_bme_time, temperature_packet, pressure_packet, humidity_packet = handle_bme_data(last_bme_time, bme280, engine, oled)
        last_pmu_time, batt_level_packet, sys_voltage_packet = handle_pmu_data(last_pmu_time, PMU, engine, oled)

        # Example of sending data from the created packets if they exist
        if gps_packet:
            send_data(gps_packet)
        if temperature_packet:
            send_data(temperature_packet)
        if pressure_packet:
            send_data(pressure_packet)
        if humidity_packet:
            send_data(humidity_packet)
        if batt_level_packet:
            send_data(batt_level_packet)
        if sys_voltage_packet:
            send_data(sys_voltage_packet)

        # Sleep to avoid busy-waiting
        time.sleep(1)

asyncio.run(main())
