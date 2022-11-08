FROM python:3.8

ADD . /

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

CMD [ "python", "-u", "./consume.py"]
