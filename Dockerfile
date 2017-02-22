# This dockerfile uses the ubuntu image
# VERSION 2 - EDITION 1
# Author: docker_user
# Command format: Instruction [arguments / command] ..

# 基本映像檔，必須是第一個指令
FROM ubuntu:16.04

# 維護者： docker_user <docker_user at email.com> (@docker_user)
MAINTAINER davidtnfsh davidtnfsh@gmail.com

ENV LANG=C.UTF-8

# 更新映像檔的指令
RUN apt-get update && \
      apt-get -y install git python3 python python3-pip wget
RUN git clone https://github.com/UDICatNCHU/KCM-Data-Source-Extractor.git
RUN pip3 install -e git://github.com/UDICatNCHU/KCM.git@master#egg=KCM

# 建立新容器時要執行的指令
CMD ["bash"]