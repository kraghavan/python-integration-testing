FROM python:3.8

WORKDIR /home

RUN apt-get update && \
    apt-get install -y python3-dev python3-pip build-essential vim && \
    pip install --upgrade pip && \
    pip install pika && \
    pip install confluent-kafka

RUN mkdir /src
COPY src/app.py /home/src/app.py

#CMD ["sleep", "infinity"]
CMD ["python", "/home/src/app.py"]