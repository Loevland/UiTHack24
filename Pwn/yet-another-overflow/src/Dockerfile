FROM ubuntu:22.04
LABEL Description="UiTHack24 Test"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY test .
COPY ynetd .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9002 ./test

# docker build -t test .
# docker run -dp 9002:9002 -it --rm test