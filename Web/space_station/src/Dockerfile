FROM python:3.8-slim
LABEL Description="UiTHack24 Space Station"
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8009
ENV NAME World
CMD ["python", "server.py"]