# This dockerfile uses the ubuntu image
# VERSION 2 - EDITION 1
# Author: docker_user
# Command format: Instruction [arguments / command] ..

# 基本映像檔，必須是第一個指令
FROM ubuntu:16.04

# 維護者： docker_user <docker_user at email.com> (@docker_user)
MAINTAINER davidtnfsh davidtnfsh@gmail.com

# 更新映像檔的指令
RUN apt-get update && apt-get install -y git 
RUN git clone https://github.com/UDICatNCHU/KCM.git
RUN make install

# the port on which we will be running app server (django runserver / gunicorn)
EXPOSE 8000

# 建立新容器時要執行的指令
CMD [python", "manage.py", "runserver"]