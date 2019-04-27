FROM python:3.6-alpine

RUN pip3 install --no-cache-dir pymongo dnspython

COPY src/ /usr/bin

cmd python -u /usr/bin/run_server.py