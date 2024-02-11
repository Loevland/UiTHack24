FROM python

WORKDIR /app/bandit
ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD ./static/ ./static/
ADD ./templates/ ./templates/
ADD ./app.py .
ADD ./flag.txt ./flag.txt
ADD ./pswd.txt ./pswd.txt
RUN mkdir ./log
RUN mkdir ./logs

EXPOSE 8888

STOPSIGNAL SIGKILL

CMD ["python", "-b", "app.py" "--port=8888", "--host=0.0.0.0"]
