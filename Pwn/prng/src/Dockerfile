FROM ubuntu:22.04
LABEL Description="UiTHack24 prng"

RUN apt-get update && apt-get upgrade -y

RUN useradd -d /home/prng -m -p prng -s /bin/bash prng
WORKDIR /home/prng

COPY ynetd .
COPY prng .
COPY flag.txt .

RUN chown -R root:root /home/prng
RUN chmod -R a+rx /home/prng

USER prng
CMD ./ynetd -p 9001 ./prng

# docker build -t prng .
# docker run -dp 9001:9001 -it --rm prng
