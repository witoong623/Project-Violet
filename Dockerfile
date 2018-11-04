FROM python:3.6.7-stretch
RUN mkdir /django
WORKDIR /django

ADD requirements.txt /django/
RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install cron mysql-client
ADD crontab /etc/cron.d/django-cron
RUN chmod 0644 /etc/cron.d/django-cron
RUN crontab /etc/cron.d/django-cron

ADD . /django/
CMD /django/start.sh
# CMD python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --env DJANGO_SETTINGS_MODULE=projectviolet.settings_prod -b 0.0.0.0:8000 projectviolet.wsgi --workers 2
