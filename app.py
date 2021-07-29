import os
import json
import requests
#from flask import Flask

def main():
    GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_SHA = os.getenv("GITHUB_SHA")

    print("sha =", GITHUB_SHA)

    data = {}

    print("Event path =",GITHUB_EVENT_PATH)
    if GITHUB_EVENT_PATH:
        with open(str(GITHUB_EVENT_PATH), 'r') as json_file:
            data = json.load(json_file)
    
    print("Data =",data)
    print("Token =",GITHUB_TOKEN)
    if data and GITHUB_TOKEN:
        username = data["sender"]["login"]
        token = GITHUB_TOKEN
        repo = data["repository"]["name"]
        ref = "refs/heads/" + data["issue"]["title"].replace(" ","_")

        url = "https://api.github.com/" + "repos/" + username + "/" + repo

        #login = requests.get("https://api.github.com/search/repositories?q=github+api", auth=(username,token))
        #print("Login status =", login)

        if GITHUB_SHA:
            headers = {
                "ref": ref,
                "sha": GITHUB_SHA
            }
            create_branch = requests.post(url, json=headers)
            print("Create branch status =",create_branch)

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