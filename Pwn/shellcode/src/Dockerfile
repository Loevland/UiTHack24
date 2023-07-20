FROM ubuntu:22.04
LABEL Description="UiTHack24 shellcode"

RUN apt-get update && apt-get upgrade -y

RUN useradd -d /home/shellcode -m -p shellcode -s /bin/bash shellcode
WORKDIR /home/shellcode

COPY ynetd .
COPY shellcode .
COPY flag.txt .

RUN chown -R root:root /home/shellcode
RUN chmod -R a+rx /home/shellcode

USER shellcode
CMD ./ynetd -p 9001 ./shellcode

# docker build -t shellcode .
# docker run -dp 9001:9001 -it --rm shellcode
