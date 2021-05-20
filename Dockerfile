 
# base image
FROM python:3.9.4

RUN mkdir /stalevar
WORKDIR /stalevar

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY . /stalevar

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
