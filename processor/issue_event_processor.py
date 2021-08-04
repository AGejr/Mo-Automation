import requests
import json
import os

from requests.models import Response
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
    repo_projects = requests.get(url=projects_url,headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER")).json()

    for project in repo_projects:
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
    response = requests.post(url=project_columns_url,json=parameters,headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER"))
    print(response.status_code, ":", response.reason)

def get_project(project_name):
    projects_url = get_projects_url()
    repo_projects = requests.get(url=projects_url,headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER")).json()

    for project in repo_projects:
        if "name" in project and project["name"] == project_name:
            return project
    return {}

def get_project_column(project_id, column_name):
    project_column_url = get_project_columns_url(project_id=project_id)
    project_column = requests.get(url=project_column_url,headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER")).json()

    for column in project_column:
        if "name" in column and column["name"] == column_name:
            return column
    return {}

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

    # If the event is an issue event where someone has been assigned
    # Then create a new issue-named branch
    if "action" in event_data and event_data["action"] == "assigned":
        create_branch_from_default_branch(issue_number=issue_number, issue_title=issue_title) 

    # If the event is an issue that has just been created, add it to the backlog in the project board
    # And if there is no project board, initialize it 
    if "state" in event_data["issue"] and event_data["issue"]["state"] == "open":
        if not get_project(ENV_VAR.config("PROJECT_BOARD_NAME")):
            initialize_project_board()
        
        add_issue_to_board_backlog(issue_id=issue_id)