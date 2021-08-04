import json
from processor import issue_event_processor
from vars.env import ENV_VAR

# TODO: Make a file with enviroment variables
# TODO: Make a predefined list API URLs 

def load_event() -> json:
    print("Loading event file")
    with open(str(ENV_VAR.config["GITHUB_EVENT_PATH"]), 'r') as json_file:
        event_data = json.load(json_file)
        print("Event data = ", event_data)
        return event_data

def main():
    event_data = load_event()
    
    # If the event is an issue related event
    if  "issue" in event_data:
        issue_event_processor.process_issue(event_data=event_data)
       
if __name__ == "__main__":
    main()