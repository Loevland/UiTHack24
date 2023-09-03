FROM ubuntu:22.04
LABEL Description="UiTHack24 overflow"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY overflow .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9001 ./overflow

# docker build -t overflow .
# docker run -dp 9001:9001 -it overflow
