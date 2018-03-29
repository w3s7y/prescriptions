FROM python:3.6
ADD requirements.txt /tmp/reqs.txt
RUN apt update && apt install -y gfortran liblapack-dev
RUN pip install numpy && pip install -r /tmp/reqs.txt
VOLUME /data
WORKDIR /data
CMD python etl.py