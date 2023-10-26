FROM ubuntu:22.04
LABEL Description="UiTHack24 Xenithian doorway"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY doorway .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9003 ./doorway

# docker build -t doorway .
# docker run -dp 9003:9003 -it doorway
