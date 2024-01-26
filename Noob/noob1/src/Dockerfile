FROM ubuntu:22.04
LABEL Description="UiTHack24 noob1"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY login .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 6000 ./login

# docker build -t noob1 .
# docker run -dp 6000:6000 -it --rm noob1
