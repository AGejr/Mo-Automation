import os
import requests

def create_issue_comment(comment_body, repo, repo_owner, issue_number, auth_header):
    parameters = {
        "issue_number": issue_number,
        "body": comment_body
    }
    url = "https://api.github.com/repos/" + repo_owner + "/" + repo + "/issues/" + str(issue_number) + "/comments"
    return requests.post(url=url,json=parameters,headers=auth_header)
    
def create_branch_from_default_branch(repo_owner, repo, issue_number, issue_title, auth_header):
    # TODO: Add check to see if branch already exists

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_SHA = os.getenv("GITHUB_SHA")

    branch_name = "issue-" + str(issue_number) + "-" + issue_title.replace(" ","_")

    if GITHUB_TOKEN and GITHUB_SHA:
        ref = "refs/heads/" + branch_name
        url = "https://api.github.com/" + "repos/" + repo_owner + "/" + repo + "/git/refs"
        parameters = {
            "ref": ref,
            "sha": GITHUB_SHA
        }

        print("Creating branch...")

        branch_status = requests.post(url=url, json=parameters, headers=auth_header)

        print("Create branch status (keys, test feature) =",branch_status.keys()) # TODO: remove testfeature

    else:
        if not GITHUB_TOKEN:
            raise Exception("ERROR: no Github token")
        elif not GITHUB_SHA:
            raise Exception("ERROR GITHUB_SHA is null")
        #elif erroneus statuscode

    comment_body = "Branch [" + branch_name + "](https://github.com/" + repo_owner + "/" + repo + "/tree/" + branch_name + ") created!"
    comment_status = create_issue_comment(comment_body, repo, repo_owner, issue_number, auth_header)
    print("Create comment status = ", comment_status)
    
# TODO: def add_issue_to_board(...)
# When a new issue is created, add it to the backlog in the Kanban board 

def process_issue(event_data, auth_header):
    repo_owner = event_data["repository"]["owner"]["login"]
    repo = event_data["repository"]["name"]
    issue_number = event_data["issue"]["number"]
    issue_title = event_data["issue"]["title"]

    # If the event is an issue event where someone has been assigned
    # Then create a new issue-named branch
    if event_data["action"] == "assigned":
        
        create_branch_from_default_branch(repo_owner, repo, issue_number, issue_title, auth_header) 

    # TODO: If the event is an issue that has just been created call add_issue_to_board 

    