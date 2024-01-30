FROM python

WORKDIR /app/bandit
ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD ./static/ ./static/
ADD ./templates/ ./templates/
ADD ./app.py .
ADD ./flag.txt /flag.txt
ADD ./pswd.txt /pswd.txt
RUN mkdir ./logs

EXPOSE 5000

STOPSIGNAL SIGKILL

CMD ["python", "-b", "app.py"]
