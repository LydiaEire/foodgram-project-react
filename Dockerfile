FROM python:3.8.5

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

ARG DJANGO_ENV=settings
ENV DJANGO_SETTINGS_MODULE=foodgram.${DJANGO_ENV}