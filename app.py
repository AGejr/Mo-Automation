import os
import json
import requests
#from flask import Flask

def main():
    GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN ")

    data = {}

    if GITHUB_EVENT_PATH:
        with open(str(GITHUB_EVENT_PATH), 'r') as json_file:
            data = json.load(json_file)
    
    if data and GITHUB_TOKEN:
        username = data["sender"]["login"]
        token = GITHUB_TOKEN
        login = requests.get("https://api.github.com/search/repositories?q=github+api", auth=(username,token))
        print(login)

if __name__ == "__main__":
    main()

"""
def create_app() -> Flask:
    app = Flask(__name__)

    GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

    if GITHUB_EVENT_PATH:
        print(GITHUB_EVENT_PATH)
        with open(str(GITHUB_EVENT_PATH), 'r') as json_file:
            data = json.load(json_file)
        print(data)

    @app.route('/some-url')
    def get_data():
        return requests.get('http://example.com').content

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
"""