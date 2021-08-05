
from requests.models import Response

from vars.env import ENV_VAR
from vars.github_api_url_getter import *
from processor.github_api_wrappers.issue import *
from processor.github_api_wrappers.project import *
from processor.github_api_wrappers.git_database import *

# TODO: Cleanup! move ever function, except for process_issue, into appropriate .py file
# E.g. create_issue_comment -> issue_something, project_board_exists -> project_something, ...

# TODO: Add caching so the app doesn't take forever!
# (might only be possible when using a selfhosted runner)

def initialize_project_board():
    projects_url = get_projects_url()
    parameters = {
            "name": ENV_VAR.config("PROJECT_BOARD_NAME")
    }
    print("Initializing automated project board...")
    response = requests.post(url=projects_url, json=parameters, headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER"))
    print(response.status_code, ":", response.reason)

    if response.status_code == 201:
        project_id = int(response.json()["id"])
        print("Creaing board columns...")
        create_project_column("Backlog", project_id)
        create_project_column("To Do", project_id)
        create_project_column("In Progress", project_id)
        create_project_column("In Review", project_id)
        create_project_column("Done", project_id)

def add_issue_to_board_backlog(issue_id):
    project_id = int(get_project(ENV_VAR.config("PROJECT_BOARD_NAME"))["id"])
    project_column_id = int(get_project_column(project_id=project_id, column_name="Backlog")["id"])
    project_cards_url = get_project_cards_url(column_id=project_column_id)
    parameters = {
        "content_id":issue_id,
        "content_type":"Issue"
    }
    print("Adding issue to backlog...")
    response = requests.post(url=project_cards_url,json=parameters,headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER"))
    print(response.status_code, ":", response.reason)

def process_issue(event_data):
    issue_number = event_data["issue"]["number"]
    issue_title = event_data["issue"]["title"]
    issue_id = event_data["issue"]["id"]

    # If the event is an issue that has just been created, add it to the backlog in the project board
    # And if there is no project board, initialize it 
    if "action" in event_data and event_data["action"] == "opened":
        if not get_project(ENV_VAR.config("PROJECT_BOARD_NAME")):
            initialize_project_board()
        
        add_issue_to_board_backlog(issue_id=issue_id)

    # If the event is an issue that has just been milestoned, move it to 'To Do'
    if "action" in event_data and event_data["action"] == "milestoned":
        move_project_card(from_column_name="Backlog", to_column_name="To Do", issue_number=issue_number)

    # If the event is an issue event where someone has been assigned
    # Then create a new issue-named branch
    if "action" in event_data and event_data["action"] == "assigned":
        create_branch_from_default_branch(issue_number=issue_number, issue_title=issue_title) 
        move_project_card(from_column_name="To Do", to_column_name="In Progress", issue_number=issue_number)

    # TODO: If issue is reopned, move to Backlog
    