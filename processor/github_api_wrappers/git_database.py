import requests
from vars.env import ENV_VAR
from vars.github_api_url_getter import *

from issue import *

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