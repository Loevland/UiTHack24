FROM ubuntu:22.04
LABEL Description="UiTHack24 shellcode"

RUN apt-get update && apt-get upgrade -y

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY shellcode .
COPY flag.txt .

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9001 ./shellcode

# docker build -t shellcode .
# docker run -dp 9001:9001 -it shellcode
