FROM python:3.8-slim-buster

WORKDIR app/

COPY requirements.txt /app
#RUN pip3 install -r /app/requirements.txt
RUN pip3 install flask 

COPY app.py /app/app.py

CMD ["ls -alF"]
CMD [ "python3", "/app/app.py"]