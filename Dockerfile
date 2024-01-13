# Use the official Python 3.9 image for ARM64 (M1)
FROM python:3.9

# Update pip and setuptools
RUN pip install --upgrade pip setuptools

# Set the working directory in the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .


# Run the image as a non-root user
CMD ["python", "App/Main.py"]
