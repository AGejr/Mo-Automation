# Github event processor

## Ngrok

### Configuration
 - Install Ngrok
 - Configure Ngrok authtoken
```
ngrok authtoken <token>
```

### Run
```
ngrok http 4567
```
(Make a note of the *.ngrok.io URL. We'll use it to set up our webhook.)

## Webhook
Setup webook:
 - Settings -> Webhooks -> Add webhook
 - Paste the *.ngrok.io URL in the payload URL
 - Select JSON content type
 - (optional) add secret
 - Select which events should trigger the webhook
 - Click Add webhook

## Flask
 - Install Flask

### Configuration
```
python -m venv venv
export FLASK_APP=event_processor
export FLASK_DEBUG=true
export FLASK_RUN_HOST=127.0.0.1
export FLASK_RUN_PORT=4567
```

### Run
```
flask run
```
