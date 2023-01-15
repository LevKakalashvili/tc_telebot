FROM python:3.10.9-slim-buster
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/LevKakalashvili/tc_telebot.git
RUN pip3 install -r "./tc_telebot/requirements.txt"
# Необходимо указать расположение .env файла на хостовой машине
# COPY ___ "./tc_telebot"
COPY .env "./tc_telebot"
RUN mkdir "./tc_telebot/app_bot/screenshots_default"
# WORKDIR "./tc_telebot"
CMD [ "python3", "./tc_telebot/app_bot/run.py"]