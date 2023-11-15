FROM ubuntu:22.04
LABEL Description="UiTHack24 noob4"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd .
COPY login .
RUN touch -- "-flag.txt "
RUN echo "UiTHack24{d4sh_31337}" > "-flag.txt "

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf

USER ctf
CMD ./ynetd -p 9001 ./login

# docker build -t noob4 .
# docker run -dp 9001:9001 -it --rm noob4
