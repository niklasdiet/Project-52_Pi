import time
from grove.gpio import GPIO

def humidify():
    # Initialize the Grove board
    gpio = GPIO()
    gpio.setup(4, GPIO.OUT)
    gpio.setup(27, GPIO.OUT)

    # Start the device attached (for example, turning on an LED)
    gpio.output(4, 1)  # Assuming pin 4 is connected to your device
    gpio.output(27, 1)  # Assuming pin 27 is connected to your device

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
        gpio.output(4, 0)
        gpio.output(27, 0)