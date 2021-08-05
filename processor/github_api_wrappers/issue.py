import requests
from vars.env import ENV_VAR
from vars.github_api_url_getter import *

# Comment

def create_issue_comment(comment_body, issue_number):
    parameters = {
        "issue_number": issue_number,
        "body": comment_body
    }
    issue_comment_url = get_issue_comment_url(issue_number=issue_number)

    print("Creating issue comment...")
    response = requests.post(url=issue_comment_url,json=parameters,headers=ENV_VAR.config("AUTH_HEADER"))
    print(response.status_code, ":", response.reason)