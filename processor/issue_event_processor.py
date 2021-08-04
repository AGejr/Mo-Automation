import requests
import json
import os
from vars.env import ENV_VAR
from vars.github_api_url_getter import *

def create_issue_comment(comment_body, issue_number):
    parameters = {
        "issue_number": issue_number,
        "body": comment_body
    }
    issue_comment_url = get_issue_comment_url(issue_number=issue_number)

    print("Creating issue comment...")
    response = requests.post(url=issue_comment_url,json=parameters,headers=ENV_VAR.config("AUTH_HEADER"))
    print(response.status_code, ":", response.reason)
    
def create_branch_from_default_branch(issue_number, issue_title):
    branch_name = "issue-" + str(issue_number) + "-" + issue_title.replace(" ","_")
    ref = "refs/heads/" + branch_name
    refs_url = get_refs_url()
    parameters = {
        "ref": ref,
        "sha": ENV_VAR.config("GITHUB_SHA")
    }

    print("Creating branch...")
    response = requests.post(url=refs_url, json=parameters, headers=ENV_VAR.config("AUTH_HEADER"))
    print(response.status_code, ":", response.reason)

    comment_body = "Branch [" + branch_name + "](https://github.com/" + ENV_VAR.config("GITHUB_REPOSITORY_OWNER") + "/" + ENV_VAR.config("GITHUB_REPOSITORY_TITLE") + "/tree/" + branch_name + ") created!"
    create_issue_comment(comment_body=comment_body, issue_number=issue_number)

# TODO: Test if the board has the appropriate columns
def project_board_exists() -> bool:
    projects_url = get_projects_url()
    header = {
        "Accept":"application/vnd.github.inertia-preview+json",
        "Authorization":"Token " + ENV_VAR.config("GITHUB_TOKEN")
    }
    repo_projects = requests.get(url=projects_url,headers=header)

    for project in repo_projects.json():
        if "name" in project and project["name"] == ENV_VAR.config("PROJECT_BOARD_NAME"):
            return True
    
    print("Automated project board couldn't be found")
    return False

def create_project_column(column_name, project_id):
    project_columns_url = get_project_columns_url(project_id=project_id)
    parameters = {
        "name": column_name
    }

    print("Creating column \"" + column_name + "\"...")
    response = requests.post(url=project_columns_url,json=parameters,headers=ENV_VAR.config("AUTH_HEADER"))
    print(response.status_code, ":", response.reason)

def initialize_project_board():
    projects_url = get_projects_url()
    parameters = {
            "name": ENV_VAR.config("PROJECT_BOARD_NAME"),
    }
    header = {
        "Accept":"application/vnd.github.inertia-preview+json",
        "Authorization":"Token " + ENV_VAR.config("GITHUB_TOKEN")
    }

    print("Initializing automated project board...")
    response = requests.post(url=projects_url, json=parameters, headers=header)
    print(response.status_code, ":", response.reason)

    if response.status_code == 201:
        project_id = int(response["id"])
        print("Creaing board columns...")
        create_project_column("Backlog", project_id)
        create_project_column("To Do", project_id)
        create_project_column("In Progress", project_id)
        create_project_column("In Review", project_id)
        create_project_column("Done", project_id)

def add_issue_to_board_backlog():
    print("*Should create branch*")    

def process_issue(event_data):
    issue_number = event_data["issue"]["number"]
    issue_title = event_data["issue"]["title"]

    # If the event is an issue event where someone has been assigned
    # Then create a new issue-named branch
    if "action" in event_data and event_data["action"] == "assigned":
        create_branch_from_default_branch(issue_number=issue_number, issue_title=issue_title) 

    # If the event is an issue that has just been created, add it to the backlog in the project board
    # And if there is no project board, initialize it 
    if "state" in event_data["issue"] and event_data["issue"]["state"] == "open":
        board_exists = project_board_exists()
        if board_exists == False:
            initialize_project_board()
        
        add_issue_to_board_backlog()

    