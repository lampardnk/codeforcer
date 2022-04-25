FROM python:3.10
WORKDIR /codeforcer

RUN apt-get update

RUN apt-get -y install sudo && apt-get -y install wget 
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN sudo mv geckodriver /usr/local/bin/

RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox

COPY . .

CMD python3 -B -u ./main.py
