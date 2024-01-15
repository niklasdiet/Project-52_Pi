FROM python:3.9

# Set the working directory in the container
WORKDIR /app


# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy the rest of the application code into the container
COPY . .

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]


