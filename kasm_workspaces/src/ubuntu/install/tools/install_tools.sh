#!/usr/bin/env bash
set -ex
if [ "$DISTRO" = centos ]; then
  yum install -y nano zip wget
  yum install epel-release -y
  yum install xdotool -y
else
  apt-get update
  apt-get install -y git # version control 
  apt-get install -y nano tmux, xdotool # editing, terminal splitting, input events
  apt-get install -y zip zlib1g-dev # compression
  apt-get install -y vlc  # multimedia
  apt-get install -y build-essential ruby-full # developer tools: gnu, ruby
fi

