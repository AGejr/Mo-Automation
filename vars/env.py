from os import getenv

class ENV_VAR:
    __conf = {
        "GITHUB_EVENT_PATH" : getenv("GITHUB_EVENT_PATH"),
        "GITHUB_API_URL" : getenv("GITHUB_API_URL"),

        "GITHUB_TOKEN" : getenv("GITHUB_TOKEN"),
        "AUTH_HEADER" : {"Authorization":"Token " + getenv("GITHUB_TOKEN")},
        "ALTERNATE_AUTH_HEADER" : {
            "Accept":"application/vnd.github.inertia-preview+json",
            "Authorization":"Token " + getenv("GITHUB_TOKEN")
        },
        "GITHUB_SHA" : getenv("GITHUB_SHA"),
        "PROJECT_BOARD_NAME" : getenv("PROJECT_BOARD_NAME", "Automated Board"),
        "GITHUB_REPOSITORY_OWNER" : getenv("GITHUB_REPOSITORY").split("/")[0],
        "GITHUB_REPOSITORY_TITLE" : getenv("GITHUB_REPOSITORY").split("/")[1],
        "GITHUB_ACTOR" : getenv("GITHUB_ACTOR")
    }

    @staticmethod
    def config(name):
        return ENV_VAR.__conf[name]
