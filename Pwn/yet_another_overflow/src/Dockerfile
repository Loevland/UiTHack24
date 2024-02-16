FROM ubuntu:22.04
LABEL Description="UiTHack24 yet another overflow"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY overflow .
COPY ynetd .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9005 ./overflow

# docker build -t overflow .
# docker run -dp 9005:9005 -it --rm overflow