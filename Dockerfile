FROM python:3.7
ADD requirements.txt /tmp/reqs.txt
RUN apt-get update && apt-get install -y gfortran liblapack-dev
RUN pip install numpy && pip install -r /tmp/reqs.txt && rm /tmp/reqs.txt
VOLUME /data
VOLUME /code
WORKDIR /data
CMD tail -f /dev/null
