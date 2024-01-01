FROM node:10.19.0
LABEL Description="UiTHack24 Space Inspector"
EXPOSE 8002

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY ["app.js", "/home/ctf/"]
COPY ["static/", "/home/ctf/static/"]

USER ctf
WORKDIR /home/ctf

RUN npm install express
CMD ["node", "app.js"]

# docker build -t space_inspector .
# docker run -dp 8002:8002 -it --rm space_inspector
