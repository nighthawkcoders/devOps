#!/usr/bin/env bash
apt-get update
apt-get install -y \
    curl \
    sudo \
    wget \
    nano \
    zip \
    build-essential \
    ruby-full \
    jupyter-notebook \
    python3 \
    python3-pip \
    python-is-python3

# Cleanup
if [ -z ${SKIP_CLEAN+x} ]; then
    apt-get autoclean
    rm -rf \
        /var/lib/apt/lists/* \
        /var/tmp/* \
        /tmp/*
fi