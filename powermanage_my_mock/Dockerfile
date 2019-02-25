FROM python:3.6-alpine

RUN pip3 install --no-cache-dir Flask

COPY src /usr/bin

CMD export FLASK_ENV=development ; export FLASK_APP=/usr/bin/powermanage.py ; flask run --host 0.0.0.0