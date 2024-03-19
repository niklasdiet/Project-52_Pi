import time
from gpiozero import OutputDevice

def humidify():

    # Initialize the Grove board
    pin4 = OutputDevice(4)
    pin27 = OutputDevice(27)

    # Start the device attached (for example, turning on an LED)
    pin4.on()  # Assuming pin 4 is connected to your device
    pin27.on()  # Assuming pin 27 is connected to your device

    try:
        # Run for 4 seconds
        start_time = time.time()
        while time.time() - start_time < 4:
            # Read sensor data or perform other operations
            time.sleep(1)  # Example: wait for 1 second before next iteration

    except KeyboardInterrupt:
        pass  # Ignore keyboard interrupt

    finally:
        # Clean up GPIO settings
        pin4.off()
        pin27.off()
