FROM python:3.8-slim-buster

WORKDIR app/

COPY requirements.txt /app
COPY app.py /app/app.py
COPY processor /app/processor
COPY vars /app/vars

RUN pip3 install -r /app/requirements.txt

CMD [ "pylint", "/app/app.py"]

CMD [ "python3", "/app/app.py"]