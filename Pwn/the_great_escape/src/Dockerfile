FROM ubuntu:22.04
LABEL Description="UiTHack24 The great escape"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY escape .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9004 ./escape

# docker build -t escape .
# docker run -dp 9004:9004 -it --rm escape
