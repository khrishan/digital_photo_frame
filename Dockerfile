FROM python:slim

LABEL maintainer="Khrishan Patel"

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

ADD app /app

WORKDIR /app

CMD [ "python", "main.py" ]
