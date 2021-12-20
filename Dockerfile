# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

ARG BOT_TOKEN
ENV BOT_TOKEN $BOT_TOKEN

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 echo_bot.py ${BOT_TOKEN}
