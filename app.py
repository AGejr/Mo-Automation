import os
import json
from flask import Flask

GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

app = Flask(__name__)

def main():
    app.run()
    print(GITHUB_EVENT_PATH)
    with open(GITHUB_EVENT_PATH, 'r') as json_file:
        data = json.load(json_file)

    print(data)

if __name__ == "__main__":
    main()
