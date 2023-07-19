FROM ubuntu:22.04
LABEL Description="UiTHack24 overflow"

#RUN apt-get update && apt-get upgrade -y

RUN useradd -d /home/overflow -m -p overflow -s /bin/bash overflow
WORKDIR /home/overflow

COPY ynetd .
COPY overflow .
COPY flag.txt .

RUN chown -R root:root /home/overflow
RUN chmod -R a+rx /home/overflow

USER overflow
CMD ./ynetd -p 9001 ./overflow

# docker build -t overflow .
# docker run -dp 9001:9001 -it overflow
