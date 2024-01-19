FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install required packages for Raspberry Pi
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-smbus i2c-tools

# Enable I2C in the Raspberry Pi configuration
RUN echo "dtparam=i2c1=on" >> /boot/config.txt && \
    echo "dtparam=i2c_arm=on" >> /boot/config.txt

# Load I2C kernel modules
RUN echo "i2c-dev" >> /etc/modules

# Copy the rest of the application code into the container
COPY . .

# Copy the Keys.cfg file into the container at /app
COPY Keys.cfg /app/

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]
