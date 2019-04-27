FROM python:2.7.15-jessie
ADD . /app
WORKDIR /app/

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

RUN apt-get -y update && \
    apt-get install -y libmysqlclient-dev cron
RUN pip install -r app/requirements.txt

RUN touch cron.log
RUN crontab crontab
RUN service cron start

ENV TZ=Europe/Vilnius
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 8080
CMD python run.py
