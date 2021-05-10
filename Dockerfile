FROM python:3.8.9-slim-buster

WORKDIR /app

ENV PORT 80

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv
RUN pipenv install

RUN sudo apt-get install python3-tk

COPY . /app

CMD [ "python", "/app/test_docker.py" ]
