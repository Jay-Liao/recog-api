FROM python:2.7

RUN apt-get update \
    && apt-get -y install vim wget 


RUN pip install Flask==0.11.1
RUN pip install flask-redis==0.3.0
RUN pip install flask-restplus==0.9.2
RUN pip install celery==4.1.0
RUN pip install gunicorn==19.6.0
RUN pip install gevent==1.2.1
RUN pip install requests==2.18.4

ADD . /opt/recog
WORKDIR /opt/recog

CMD tail -f /dev/null