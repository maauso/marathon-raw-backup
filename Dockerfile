FROM alpine:latest

LABEL authors="Miguel Ángel Ausó <m.auso.p@gmail.com>"

RUN apk add --update python py-pip \
    && pip install requests

COPY marathon-raw-backup.py /marathon-raw-backup.py
RUN chmod 777 marathon-raw-backup.py

CMD ["sh","-c","/usr/bin/python /marathon-raw-backup.py --environment ${ENVIRONMENT} --url ${URL}"] 
