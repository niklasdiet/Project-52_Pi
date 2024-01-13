FROM arm64v8/python:3.9-slim

# Continue with the rest of your Dockerfile
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install firebase_admin

#RUN pip install -r requirements.txt

COPY . /app

# Run the image as a non-root user
CMD ["python", "App/Main.py"]
