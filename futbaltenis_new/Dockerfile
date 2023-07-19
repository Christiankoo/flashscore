FROM python:3.9

WORKDIR /app

RUN apt-get -y update
RUN pip install --upgrade pip
RUN apt-get install zip -y
RUN apt-get install unzip -y

COPY requirements.txt /app
#COPY test.py /app
COPY chromedriver /app

RUN pip3 install --no-cache-dir -r requirements.txt
RUN mv chromedriver /usr/bin/chromedriver
RUN chmod 0755 /usr/bin/chromedriver

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable



