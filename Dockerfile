# Build Stage
FROM python:3.9-alpine AS build

# Set the working directory in the container
WORKDIR /app

# Create and activate a Python virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final Stage
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary artifacts from the build stage
COPY --from=build /opt/venv /opt/venv
COPY --from=build /app /app

# Copy the Keys.cfg file into the container at /app
COPY Keys.cfg /app/

# Run the image as a non-root user
CMD ["python", "App/Main.py"]
