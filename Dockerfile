FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt


# Install required packages for Raspberry Pi
RUN apt-get update


RUN pip install --upgrade pip

RUN pip install picamera2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the gpio group
#RUN groupadd -r gpio

# Create a non-root user and add it to the gpio and i2c groups
#RUN useradd -r -g gpio -G i2c -m -s /bin/bash project52
#RUN usermod -aG i2c project52

# Switch to the non-root user
USER project52

# Copy the rest of the application code into the container
COPY /RaspberryPi/App /app

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]


