FROM python:3.6

RUN pip3 install --no-cache-dir pymongo dnspython

ENV CONF_FILE /mnt/server_config.ini

COPY src/ /usr/bin

CMD python -u /usr/bin/run_server.py