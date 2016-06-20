FROM python:3.5-onbuild
MAINTAINER mathieu@buffenoir.tech

WORKDIR /usr/src/app

RUN pip3 install two1

VOLUME /root/.two1/

EXPOSE 5000

CMD ["python3","./app.py"]