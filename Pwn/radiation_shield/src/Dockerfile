FROM ubuntu:22.04
LABEL Description="UiTHack24 Radiation shield"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY shield .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9000 ./shield

# docker build -t shield .
# docker run -dp 9000:9000 -it shield
