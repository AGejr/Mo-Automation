import os
import json
from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)

    GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

    if GITHUB_EVENT_PATH:
        print(GITHUB_EVENT_PATH)
        with open(str(GITHUB_EVENT_PATH), 'r') as json_file:
            data = json.load(json_file)
        print(data)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()