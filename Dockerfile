# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

ENV BOT_TOKEN $BOT_TOKEN

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 bot.py $BOT_TOKEN
