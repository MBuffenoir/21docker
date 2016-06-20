FROM python:3.5-onbuild
MAINTAINER mathieu@buffenoir.tech

WORKDIR /usr/src/app

RUN pip3 install two1

ENV C_FORCE_ROOT True

CMD ["celery", "-A", "worker", "worker", "-B", "--loglevel=INFO"]