FROM ubuntu:latest

# Install Python and Pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install the latest version of Python
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade setuptools && \
    python3 -m pip install --upgrade wheel && \
    apt-get install -y python3.9

# Continue with the rest of your Dockerfile
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# Run the image as a non-root user
CMD ["python3.9", "App/Main.py"]
