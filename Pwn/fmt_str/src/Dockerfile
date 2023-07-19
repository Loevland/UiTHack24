FROM ubuntu:22.04
LABEL Description="UiTHack24 Format"

RUN apt-get update && apt-get upgrade -y

RUN useradd -d /home/format -m -p format -s /bin/bash format
WORKDIR /home/format

COPY fmt .
COPY ynetd .
COPY flag.txt .

RUN chown -R root:root /home/format
RUN chmod -R a+rx /home/format

USER format
CMD ./ynetd -p 9001 ./fmt

# docker build -t format .
# docker run -dp 9001:9001 -it --rm format
