#!/usr/bin/env bash
set -ex
if [ "$DISTRO" = centos ]; then
  yum install -y nano zip wget
  yum install epel-release -y
  yum install xdotool -y
else
  apt-get update
  apt-get install -y nano zip xdotool
  apt-get install -y vlc git tmux
  apt-get install ruby-full build-essential zlib1g-dev -y
fi

