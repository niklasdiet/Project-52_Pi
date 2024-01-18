# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Add a non-root user (replace "your_username" with your desired username)
RUN groupadd -r i2c && useradd -r -g i2c -G sudo -m niklasdiet

# Change the ownership of the working directory to the non-root user
RUN chown -R niklasdiet:i2c /app

# Grant read and write permissions to the I2C device
RUN chmod 666 /dev/i2c-1

# Specify the user to run the container as
USER niklasdiet

# Copy the current directory contents into the container at /app
COPY . /app

# Run the image as a non-root user
CMD ["python", "App/Main.py"]


