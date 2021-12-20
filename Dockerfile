FROM ubuntu:latest

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        xvfb \ 
        python3-pip \
        libglib2.0-0 \
        libnss3 \
        libgconf-2-4 \
        libfontconfig1 \
        wget \
        firefox \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libatspi2.0-0 \
        libcairo2 \
        libcups2 \
        libcurl3-gnutls \
        libcurl3-nss \
        libcurl4 \
        libgbm1 \
        libgtk-3-0 \
        libpango-1.0-0 \
        libxcomposite1 \
        libxdamage1 \
        libxkbcommon0 \
        libxrandr2 \
        xdg-utils \
        htop \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb

ADD ./cryptogodz_bot /app
ADD ./requirements.txt /app
ADD ./run.py /app
ADD ./docker-entrypoint.py /app

WORKDIR /app

ENV DISPLAY=:1
RUN pip install -r requirements.txt \
    && chmod +x docker-entrypoint.sh

CMD ./docker-entrypoint.sh
