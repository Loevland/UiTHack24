FROM ubuntu:22.04
LABEL Description="UiTHack24 noob5"

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
RUN useradd -d /home/elite -m -p sup3rdup3r1mp0ss1bl3p4ssw0rd! -s /bin/bash elite
WORKDIR /home/ctf

COPY ynetd .
COPY login .
COPY flag.txt .
RUN cp /usr/bin/cat /home/elite/cat

RUN chown -R root:root /home/ctf
RUN chmod -R a+rx /home/ctf
RUN chown -R root:root /home/elite
RUN chmod -R a+rx /home/elite

RUN chown root:elite /home/ctf/flag.txt
RUN chmod 440 /home/ctf/flag.txt

RUN chown root:elite /home/elite/cat
RUN chmod u+s /home/elite/cat

USER ctf
CMD ./ynetd -p 6004 ./login

# docker build -t noob5 .
# docker run -dp 6004:6004 -it --rm noob5
