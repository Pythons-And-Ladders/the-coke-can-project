import asyncio
import aioble
import bluetooth

# Define UUIDs for the BLE service and characteristic.
MESSAGE_SERVICE_UUID = bluetooth.UUID(0x1234)
MESSAGE_CHARACTERISTIC_UUID = bluetooth.UUID(0x1235)

# Create a GATT server with a characteristic to receive messages
# MESSAGE_SERVICE is the BLE service, and MESSAGE_CHARACTERISTIC is the BLE characteristic
MESSAGE_SERVICE = aioble.Service(MESSAGE_SERVICE_UUID)
MESSAGE_CHARACTERISTIC = aioble.Characteristic(MESSAGE_SERVICE, MESSAGE_CHARACTERISTIC_UUID, write=True)

# Register the GATT service so that the BLE server is aware of this service and characteristic
aioble.register_services(MESSAGE_SERVICE)

# Asynchronous task to handle received messages from the client
async def MESSAGE_TASK(CONNECTION):
    try:
        # Keep the connection open and listen for incoming messages indefinitely
        with CONNECTION.timeout(None):  # Timeout set to None (but configurable to any time)
            while True:
                # Wait for the client to write data to the characteristic (non-blocking)
                await MESSAGE_CHARACTERISTIC.written()
                
                # Read the message written to the characteristic, decode it, and print it
                MSG = MESSAGE_CHARACTERISTIC.read().decode()
                print(f"Received message: {MSG}")

    # If the client disconnects, this exception will be caught, and the task will stop
    except aioble.DeviceDisconnectedError:
        print("Client disconnected.")
        return

# Asynchronous task to handle advertising and waiting for client connections
async def PERIPHERAL_TASK():
    while True:
        print("Waiting for a connection...")

        # Start BLE advertising to allow clients to find and connect to this server
        # The server advertises the name "BLE-Message-Server" and the service UUID
        CONNECTION = await aioble.advertise(500000, name="BLE-Message-Server", services=[MESSAGE_SERVICE_UUID])
        
        # Once a client connects, print the device information
        print("Connected to:", CONNECTION.device)

        # Start the task to handle receiving messages after a connection is established
        await MESSAGE_TASK(CONNECTION)

# Main function to start the peripheral task.
async def MAIN():
    # Start the peripheral task, which will handle the advertising and connections
    await PERIPHERAL_TASK()

# Run the BLE server and handle KeyboardInterrupt to allow clean exit
try:
    asyncio.run(MAIN())  # Start the asynchronous loop with the main task
except KeyboardInterrupt:
    # Handle the case where the program is interrupted (Ctrl+C), and exit.
    print("\nProgram interrupted. Exiting...")

