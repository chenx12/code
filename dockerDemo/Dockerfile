FROM python

COPY requirements.txt /home/
COPY proto_buf  /home/proto_buf

RUN  pip install -r /home/requirements.txt \
     && apt-get update \
     && apt-get install -y vim 



