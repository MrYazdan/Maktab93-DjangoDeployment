FROM python:3.11.0-bullseye
LABEL maintainer="mrrezayazdani@yahoo.com"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt update -y
RUN pip install -r requirements.txt