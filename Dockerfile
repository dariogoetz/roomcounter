FROM python:3.8

ADD app /app

EXPOSE 80

WORKDIR /app

# required for raspberry pi
# RUN apt-get update && apt-get install -y libzmq3-dev

# RUN python3 setup.py install
RUN pip install poetry

RUN poetry install

ENV PYTHONPATH=.

CMD poetry run uvicorn roomcounter.main:app --host 0.0.0.0 --port 80
