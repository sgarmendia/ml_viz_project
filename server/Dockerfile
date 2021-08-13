#  Dockerfile for CORE BDML project 1

FROM python:3.9.4

#Create folder for container
WORKDIR /api

# Copy files to container
ADD . .

# Install requirements
RUN  pip install -r requirements.txt

# Entry command
CMD ["python","app.py"]