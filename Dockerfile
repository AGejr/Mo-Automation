FROM python:3.8-slim-buster

WORKDIR app/

COPY requirements.txt /app
#RUN pip3 install -r /app/requirements.txt
RUN pip3 install flask 
# Networking error ^

COPY app.py /app

CMD [ "python3", "-m" , "flask", "run"]