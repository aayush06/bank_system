FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /bank_system
RUN apt-get update
RUN apt-get install -y gdal-bin
WORKDIR /bank_system
COPY requirements.txt /bank_system/
RUN pip install -r requirements.txt
COPY . /bank_system/