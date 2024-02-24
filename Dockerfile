# Use a minimal base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
RUN apt-get update && \
    apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libavfilter-dev libswscale-dev libswresample-dev libcap-dev

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Check if the system is a Raspberry Pi before installing picamera
RUN if [ "$(cat /proc/cpuinfo | grep Raspberry)" != "" ]; then \
        pip install --no-cache-dir picamera==1.13; \
    else \
        echo "Not installing picamera as this is not a Raspberry Pi"; \
    fi



# Create a non-root user and switch to it
RUN useradd -m -r -s /bin/bash project52
USER project52

# Copy the rest of the application code into the container
COPY . .

# Display system architecture
RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]