FROM python:3.10.7-slim
WORKDIR /back
COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

COPY ./ /back
