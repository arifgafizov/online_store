FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /web_django/
WORKDIR /web_django/

COPY . /web_django/
RUN pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn online_store.wsgi:application --name app --bind 0.0.0.0:8000 --workers 6 --log-level=info -t 600 --capture-output