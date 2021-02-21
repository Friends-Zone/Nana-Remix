# We're using Debian Slim Buster image
FROM python:3.9.0-slim-buster

ENV PIP_NO_CACHE_DIR 1
ENV DEBIAN_FRONTEND noninteractive

RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# Installing Required Packages
RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    debian-keyring \
    debian-archive-keyring \
    bash \
    curl \
    git \
    util-linux \
    libffi-dev \
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libwebp-dev \
    linux-headers-amd64 \
    musl-dev \
    musl \
    neofetch \
    python3-lxml \
    postgresql \
    postgresql-client \
    libpq-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libxslt1-dev \
    openssl \
    pv \
    jq \
    wget \
    python3-dev \
    libreadline-dev \
    libyaml-dev \
    zlib1g \
    ffmpeg \
    libssl-dev \
    libgconf-2-4 \
    libxi6 \
    zlib1g-dev \
    xvfb \
    unzip \
    make \
    libopus0 \
    libopus-dev \
    gcc \
    && rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

# Pypi package Repo upgrade
RUN pip3 install --upgrade pip setuptools wheel

# Clone the fork to the workspace folder.
RUN git clone https://github.com/MadeByThePinsHub/Nana-Remix /app
WORKDIR /app

# Use env vars by default, because we're using Docker
# containners after all.
ENV ENV True

# Install deps using our Makefile
RUN make install

# Starting Worker
CMD ["make","run"]
