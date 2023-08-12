FROM ubuntu:22.04
LABEL Description="UiTHack24 prng"

RUN apt-get update && apt-get upgrade -y

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY prng .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9001 ./prng

# docker build -t prng .
# docker run -dp 9001:9001 -it prng
