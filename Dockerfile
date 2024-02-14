FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt


# Install required packages for Raspberry Pi
RUN apt-get update && \
    apt-get install -y libavformat-dev && \
    apt-get install -y libavcodec-dev && \
    apt-get install -y libavdevice-dev && \
    apt-get install -y libavutil-dev && \
    apt-get install -y libavfilter-dev && \
    apt-get install -y libswscale-dev && \
    apt-get install -y libswresample-dev && \
    apt-get install -y libcap-dev && \
    apt-get install -y build-essential cmake

RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools

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


