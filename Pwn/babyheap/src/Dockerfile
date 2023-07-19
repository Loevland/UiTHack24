FROM ubuntu:22.04
LABEL Description="UiTHack24 babyheap"

RUN apt-get update && apt-get upgrade -y

RUN useradd -d /home/babyheap -m -p babyheap -s /bin/bash babyheap
WORKDIR /home/babyheap

COPY ynetd .
COPY babyheap .
COPY flag.txt .

RUN chown -R root:root /home/babyheap
RUN chmod -R a+rx /home/babyheap

USER babyheap
CMD ./ynetd -p 9001 ./babyheap

# docker build -t babyheap .
# docker run -dp 9001:9001 -it --rm babyheap
