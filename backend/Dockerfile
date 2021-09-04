FROM python:3.8.5
WORKDIR /code
COPY requirements /code
RUN pip install -r /code/requirements
COPY . /code
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000