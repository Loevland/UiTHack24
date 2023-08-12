FROM node:10.19.0
LABEL Description="UiTHack24 Traversal"
EXPOSE 9001

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ["app.js", "flag.txt", "/home/ctf/"]
COPY ["static/", "/home/ctf/static/"]

USER ctf
WORKDIR /home/ctf

RUN npm install express
CMD ["node", "app.js"]

# docker build -t traversal .
# docker run -dp 9001:9001 -it --rm traversal
