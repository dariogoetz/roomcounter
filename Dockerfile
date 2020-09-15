FROM python:latest

ADD app /app

EXPOSE 80

WORKDIR /app

# required for raspberry pi
# RUN apt-get update && apt-get install -y libzmq3-dev

# RUN python3 setup.py install
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

RUN poetry install

RUN apt-get update && apt-get install -y zip

ENV PYTHONPATH=.

CMD poetry run uvicorn roomcounter.main:app --port 80
