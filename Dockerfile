FROM python:3.9


RUN apt-get update && \
	apt-get install python-pip libatlas3-base -y && \
	pip install -U pip

# Continue with the rest of your Dockerfile
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# Run the image as a non-root user
CMD ["python", "App/Main.py"]
