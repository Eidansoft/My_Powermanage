FROM python:3.6-alpine

RUN pip3 install --no-cache-dir bottle xmltodict

COPY src /usr/bin

CMD python /usr/bin/powermanage.py