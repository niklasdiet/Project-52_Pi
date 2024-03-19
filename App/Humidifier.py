import time
import mraa
def humidify():


    # Initialize the Grove board
    gpio4 = mraa.Gpio(4)
    gpio4.dir(mraa.DIR_OUT)
    gpio27 = mraa.Gpio(27)
    gpio27.dir(mraa.DIR_OUT)

    # Start the device attached (for example, turning on an LED)
    gpio4.write(1)  # Assuming pin 4 is connected to your device
    gpio27.write(1)  # Assuming pin 27 is connected to your device

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
        gpio4.write(0)
        gpio27.write(0)
