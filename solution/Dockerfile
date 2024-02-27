FROM python:3.12.1-alpine3.19

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SERVER_ADDRESS = 0.0.0.0
ENV SERVER_PORT=8080
ENV DJANGO_DEBUG = False

RUN pip3 install --upgrade pip
COPY requirements/prod.txt .
RUN pip3 install -r prod.txt

WORKDIR /app

COPY . .

CMD ["sh", "-c", "cd pulse && exec python3 manage.py runserver $SERVER_ADDRESS:$SERVER_PORT"]
