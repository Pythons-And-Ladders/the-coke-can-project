import asyncio
import aioble
import bluetooth

# UUIDs for the BLE service and characteristic
MESSAGE_SERVICE_UUID = bluetooth.UUID(0x1234)
MESSAGE_CHARACTERISTIC_UUID = bluetooth.UUID(0x1235)

class MessageClient:
    # Initialise the MessageClient
    def __init__(self, device):
        self._device = device    # Define the BLE server device to connect to
        self._connection = None  # Placeholder for the connection object
    
    # Asynchronously connect to the specified device
    async def connect(self):
        print(f"Connecting to {self._device}...")
        self._connection = await self._device.connect() # Establish connection with BLE server device
        print("Discovering services...")
        # Discover the service on the connected device using its UUID
        MESSAGE_SERVICE = await self._connection.service(MESSAGE_SERVICE_UUID)
        # Discover the characteristic (for sending/receiving data) within the service
        self._message_characteristic = await MESSAGE_SERVICE.characteristic(MESSAGE_CHARACTERISTIC_UUID) 

    # Asynchronously send a message to the device via the characteristic
    async def send_message(self, MESSAGE):
        print(f"Sending message: {MESSAGE}")
        await self._message_characteristic.write(MESSAGE.encode()) # Encode the the message and write to the characteristic

    # Disconnect from the device when called if a connection exists
    async def disconnect(self):
        if self._connection:
            await self._connection.disconnect() # Disconnect from connected device

# Scan for the server and send a message.
async def main():
    # Scan for BLE devices
    async with aioble.scan(5000, 30000, 30000, active=True) as scanner:
        # Loop through each device within scan results
        async for result in scanner:
            # Check if the device matches the "BLE-Message-Server" and service UUID
            if result.name() == "BLE-Message-Server" and MESSAGE_SERVICE_UUID in result.services():
                # Store the device for connection
                device = result.device
                break # Break out of loop when desired device has been found
        else:
            # If no devices with the desired name and service UUID are found then print results
            print("BLE server not found.")
            return
        
    message = 'TestingBLE'               # Message to be sent
    client = MessageClient(device)       # Create an instance of the MessageClient class with the result device
    await client.connect()               # Connect to the BLE server device
    await client.send_message(message)   # Send the message to the BLE server device
    print("Message sent")                # Print confirmation of sent message
    await client.disconnect()            # Disconnect from the BLE server device

# Run the main function in an asynchronous loop
asyncio.run(main())
