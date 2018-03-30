FROM python:3.6

RUN pip install requests

ADD in.bash /opt/resource/in
ADD out.bash /opt/resource/out
ADD check.bash /opt/resource/check
RUN chmod -R 755 /opt/resource

