FROM node:10.19.0
LABEL Description="UiTHack24 Space traverse"
EXPOSE 8000

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ["app.js", "flag.txt", "/home/ctf/"]
COPY ["static/", "/home/ctf/static/"]

USER ctf
WORKDIR /home/ctf

RUN npm install express
CMD ["node", "app.js"]

# docker build -t space_traverse .
# docker run -dp 8000:8000 -it --rm space_traverse
