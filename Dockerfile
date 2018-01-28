FROM python:3.6-alpine

WORKDIR /app

RUN pip install pika

ADD ping.py /app/ping.py

CMD ["python3", "ping.py"]
