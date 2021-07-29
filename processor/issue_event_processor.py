import os
import requests

def create_branch_from_default_branch(username, repo, issue_number, issue_title, auth_header):
    # TODO: Add check to see if branch already exists

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_SHA = os.getenv("GITHUB_SHA")

    branch_name = "issue-" + str(issue_number) + "-" + issue_title.replace(" ","_")

    if GITHUB_TOKEN and GITHUB_SHA:
        ref = "refs/heads/" + branch_name
        url = "https://api.github.com/" + "repos/" + username + "/" + repo + "/git/refs"
        parameters = {
            "ref": ref,
            "sha": GITHUB_SHA
        }

        print("Creating branch...")

        create_branch = requests.post(url=url, json=parameters, headers=auth_header)

        print("Create branch status =",create_branch)

    else:
        if not GITHUB_TOKEN:
            raise Exception("ERROR: no Github token")
        elif not GITHUB_SHA:
            raise Exception("ERROR GITHUB_SHA is null")

    comment_body = "Branch [" + branch_name + "](https://github.com/" + username + "/" + repo + "/tree/" + branch_name + ") created!"
    parameters = {
        "issue_number": issue_number,
        "body": comment_body
    }
    url = "https://api.github.com/repos/" + username + "/" + repo + "/issues/" + str(issue_number) + "/comments"
    print("Creating comment on issue...")
    create_comment = requests.post(url=url,json=parameters,headers=auth_header)
    print("Create comment status = ", create_comment)

def process_issue(event_data, auth_header):

    # If the event is an issue event where someone has been assigned
    # Then create a new issue-named branch
    if event_data["action"] == "assigned":
        username = event_data["sender"]["login"]
        repo = event_data["repository"]["name"]
        issue_number = event_data["issue"]["number"]
        issue_title = event_data["issue"]["title"]
        create_branch_from_default_branch(username, repo, issue_number, issue_title, auth_header) 