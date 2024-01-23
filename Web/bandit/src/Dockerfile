FROM python

WORKDIR /app/placeholder
ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD ./static/ ./static/
ADD ./templates/ ./templates/
ADD ./app.py .
ADD ./flag.txt /flag.txt
ADD ./pswd.txt /pswd.txt
RUN mkdir /log

EXPOSE 5000

STOPSIGNAL SIGKILL

CMD ["python", "-b", "app.py"]
