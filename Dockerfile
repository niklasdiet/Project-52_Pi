# Use the official Python 3.9 image for ARM64 (M1)
FROM python:3.9

# Update pip and setuptools
RUN pip install --upgrade pip setuptools

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Maturin
RUN pip install maturin

# Copy the pyproject.toml and src directory into the container
COPY pyproject.toml .
COPY src ./src

# Build the Rust Python extension
RUN maturin develop

# Install any dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt



# Copy the rest of the application code into the container
COPY . .

RUN uname -m

# Run the image as a non-root user
CMD ["python", "App/Main.py"]

