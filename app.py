import os
import json
import requests

GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_SHA = os.getenv("GITHUB_SHA")

def load_event() -> json:
    if GITHUB_EVENT_PATH:
        print("Loading event file")
        with open(str(GITHUB_EVENT_PATH), 'r') as json_file:
            return json.load(json_file)
    else:
        raise Exception("ERROR: event file was not loaded")

def create_branch_from_default_branch(username, repo, issue_title, auth_header):
    # TODO: Add check to see if branch already exists

    if GITHUB_TOKEN and GITHUB_SHA:
        ref = "refs/heads/" + issue_title.replace(" ","_")
        url = "https://api.github.com/" + "repos/" + username + "/" + repo + "/git/refs"

        parameters = {
            "ref": ref,
            "sha": GITHUB_SHA
        }

        print("Creating branch...")

        create_branch = requests.post(url, json=parameters, headers=auth_header)

        print("Create branch status =",create_branch)

    else:
        if not GITHUB_TOKEN:
            raise Exception("ERROR: no Github token")
        elif not GITHUB_SHA:
            raise Exception("ERROR GITHUB_SHA is null")


def main():
    auth_header = {
                "Authorization": "Token " + GITHUB_TOKEN
    }

    event_data = load_event()

    # If the event is an issue event where someone has been assigned
    if  "issue" in event_data and event_data["action"] == "assigned":
        username = event_data["sender"]["login"]
        repo = event_data["repository"]["name"]
        issue_title = "issue-" + str(event_data["issue"]["number"]) + "-" + event_data["issue"]["title"]
        create_branch_from_default_branch(username, repo, issue_title, auth_header) 
       
if __name__ == "__main__":
    main()