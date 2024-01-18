FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install required packages for Raspberry Pi
RUN apt-get update && apt-get install -y --no-install-recommends raspi-config
RUN raspi-config nonint do_i2c 0
RUN apt-get install -y python3-smbus i2c-tools

# Copy the rest of the application code into the container
COPY . .

# Copy the Keys.cfg file into the container at /app
COPY Keys.cfg /app/

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]


