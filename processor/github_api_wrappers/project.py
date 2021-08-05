import requests
from vars.env import ENV_VAR
from vars.github_api_url_getter import *

# Project

def get_project(project_name):
    projects_url = get_projects_url()
    repo_projects = requests.get(url=projects_url,headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER")).json()

    for project in repo_projects:
        if "name" in project and project["name"] == project_name:
            return project
    return

# Column

def get_project_column(project_id, column_name):
    project_column_url = get_project_columns_url(project_id=project_id)
    project_column = requests.get(url=project_column_url,headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER")).json()

    for column in project_column:
        if "name" in column and column["name"] == column_name:
            return column
    return

def create_project_column(column_name, project_id):
    project_columns_url = get_project_columns_url(project_id=project_id)
    parameters = {
        "name": column_name
    }
    print("Creating column \"" + column_name + "\"...")
    response = requests.post(url=project_columns_url,json=parameters,headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER"))
    print(response.status_code, ":", response.reason)

# Cards

def get_project_card(column_id, issue_number):
    project_cards_url = get_project_cards_url(column_id=column_id)
    project_cards = requests.get(url=project_cards_url, headers=ENV_VAR.config("ALTERNATE_AUTH_HEADER")).json()
    for project_card in project_cards:
        if "content_url" in project_card:
            linked_issue_number = int(project_card["content_url"].split("/")[-1])
            if linked_issue_number == issue_number:
                return project_card
    return