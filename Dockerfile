FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN sudo pip install adafruit-circuitpython-bme680

# Install required packages for Raspberry Pi
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-smbus i2c-tools

# Copy the rest of the application code into the container
COPY . .

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]


