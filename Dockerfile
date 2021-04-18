FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /web_django/
WORKDIR /web_django/

COPY . /web_django/
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "./manage.py", "runserver" , "0.0.0.0:8000"]