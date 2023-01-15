FROM python:3.10

# ставим google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# ставим chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# обновляем pip
RUN pip install --upgrade pip

# ставим git
USER root
RUN apt-get update && apt-get install -y git

# клонируем проект
RUN git clone https://github.com/LevKakalashvili/tc_telebot.git

RUN pip3 install -r "./tc_telebot/requirements.txt"

# копируем .env с хоста
# необходимо указать расположение .env файла на хостовой машине
# COPY ___ "./tc_telebot"
COPY .env "./tc_telebot"
RUN mkdir "./tc_telebot/app_bot/screenshots_default"

# запускаем проект
CMD [ "python3", "./tc_telebot/app_bot/run.py"]