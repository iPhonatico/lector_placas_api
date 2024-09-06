FROM amancevice/pandas:slim-2.1.3

ENV PYTHONUNBUFFERED 1
ENV TZ=America/Guayaquil

RUN apt-get update -y


RUN mkdir /code

WORKDIR /code

RUN apt-get update
RUN apt-get install -y build-essential binutils python3-opencv

ADD requierements.txt /code/
RUN pip install --upgrade pip
RUN pip3 install -r requierements.txt

ADD . /code/