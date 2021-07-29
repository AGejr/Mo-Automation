import os
import json
import requests
from processor import issue_event_processor
from processor import pr_event_processor

def load_event() -> json:

    GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

    if GITHUB_EVENT_PATH:
        print("Loading event file")
        with open(str(GITHUB_EVENT_PATH), 'r') as json_file:
            return json.load(json_file)
    else:
        raise Exception("ERROR: event file was not loaded")

def main():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    auth_header = {
                "Authorization": "Token " + GITHUB_TOKEN
    }

    event_data = load_event()

    # If the event is an issue related event
    if  "issue" in event_data:
        issue_event_processor.process_issue(event_data=event_data, auth_header=auth_header)
       
if __name__ == "__main__":
    main()