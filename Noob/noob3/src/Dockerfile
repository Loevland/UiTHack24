FROM ubuntu:22.04
LABEL Description="UiTHack24 noob3"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY login .
COPY .bash_history .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 6002 ./login

# docker build -t noob3 .
# docker run -dp 6002:6002 -it --rm noob3
