# Build Stage
FROM python:3.9-alpine AS build

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Final Stage
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary artifacts from the build stage
COPY --from=build /app /app

# Install required packages for Raspberry Pi
RUN apk add --no-cache i2c-tools

# Manually grant permissions for I2C
RUN chmod 666 /dev/i2c-1

# Run the image as a non-root user
CMD ["python", "App/Main.py"]
