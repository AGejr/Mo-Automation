from vars.env import ENV_VAR

def get_issue_comment_url(issue_number):
    return "https://api.github.com/repos/" + ENV_VAR.config("GITHUB_REPOSITORY_OWNER") + "/" + ENV_VAR.config("GITHUB_REPOSITORY_TITLE") + "/issues/" + str(issue_number) + "/comments"

def get_refs_url():
    return "https://api.github.com/" + "repos/" + ENV_VAR.config("GITHUB_REPOSITORY_OWNER") + "/" + ENV_VAR.config("GITHUB_REPOSITORY_TITLE") + "/git/refs"

def get_projects_url():
    return "https://api.github.com/repos/" + ENV_VAR.config("GITHUB_REPOSITORY_OWNER") + "/" + ENV_VAR.config("GITHUB_REPOSITORY_TITLE") + "/projects"

def get_project_columns_url(project_id):
    return "https://api.github.com/projects/" + str(project_id) + "/columns"

def get_project_cards_url(column_id):
    return "https://api.github.com/projects/columns/" + str(column_id) + "/cards"