FROM python:3.9-alpine


# Set the working directory in the container
WORKDIR /app

# Install required packages for Raspberry Pi
RUN apt-get update && apt-get install -y --no-install-recommends
RUN apk add --no-cache i2c-tools

# Install any dependencies specified in requirements.txt
#COPY requirements.txt .
#RUN pip install -r requirements.txt

RUN pip install pymongo
RUN pip install requests
RUN pip install bme680
RUN pip install adafruit-circuitpython-bme680
RUN pip install RPi.GPIO



# Manually grant permissions for I2C
RUN chmod 666 /dev/i2c-1

# Copy the rest of the application code into the container
COPY . .

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]
