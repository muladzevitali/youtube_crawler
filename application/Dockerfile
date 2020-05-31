FROM python:3.8.1

WORKDIR /usr/src/application

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/application/requirements.txt
RUN pip install -r requirements.txt
