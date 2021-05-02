FROM python:3.8-slim
WORKDIR /backend

ENV PYTHONUNBUFFERED 1

# Install apt dependencies
RUN apt update
RUN apt install -y libpq-dev gcc wget unzip curl

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8888

COPY . /backend