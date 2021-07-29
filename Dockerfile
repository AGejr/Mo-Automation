FROM python:3.8-slim-buster

WORKDIR app/

COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

COPY app.py /app/app.py

CMD [ "python3", "/app/app.py"]