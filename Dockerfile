FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
RUN apt-get update && \
    apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libavfilter-dev libswscale-dev libswresample-dev libcap-dev

# Install build dependencies
RUN apt-get install -y build-essential

# Install CMake from source
RUN wget https://cmake.org/files/v3.21/cmake-3.21.3-Linux-x86_64.tar.gz && \
    tar -zxvf cmake-3.21.3-Linux-x86_64.tar.gz && \
    cp -r cmake-3.21.3-Linux-x86_64/* /usr && \
    rm -rf cmake-3.21.3-Linux-x86_64 && \
    rm cmake-3.21.3-Linux-x86_64.tar.gz

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the gpio group
#RUN groupadd -r gpio

# Create a non-root user and add it to the gpio and i2c groups
#RUN useradd -r -g gpio -G i2c -m -s /bin/bash project52
#RUN usermod -aG i2c project52

# Switch to the non-root user
#USER project52

# Copy the rest of the application code into the container
COPY /RaspberryPi/App /app

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]


