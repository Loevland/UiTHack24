FROM ubuntu 

RUN apt-get update 
RUN apt-get install python3-pip
RUN apt-get install flask

ADD server.py /
ADD database.sqlite /
WORKDIR /

EXPOSE 5000

CMD [“python3”,”server.py”]