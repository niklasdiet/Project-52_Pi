FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install required packages for Raspberry Pi
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-smbus i2c-tools

# Create the gpio group
RUN groupadd -r gpio

# Create a non-root user and add it to the gpio and i2c groups
RUN useradd -r -g gpio -G i2c -m -s /bin/bash project52
RUN usermod -aG i2c project52

# Switch to the non-root user
USER project52

# Copy the rest of the application code into the container
COPY . .

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]


