FROM node:10.19.0
LABEL Description="UiTHack24 Traversal"
EXPOSE 9001

# User
RUN adduser --disabled-password --gecos "" traversal

COPY ["app.js", "flag.txt", "/home/traversal/"]
COPY ["static/", "/home/traversal/static/"]

USER traversal
WORKDIR /home/traversal

RUN npm install express
CMD ["node", "app.js"]
