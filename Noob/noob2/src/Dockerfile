FROM ubuntu:22.04
LABEL Description="UiTHack24 noob2"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY login .
RUN mkdir .secret
COPY .secret/flag.txt .secret

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9001 ./login

# docker build -t noob2 .
# docker run -dp 9001:9001 -it --rm noob2
