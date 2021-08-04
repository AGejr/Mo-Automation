import os

class ENV_VAR:
    __conf = {
        "GITHUB_EVENT_PATH" : os.getenv("GITHUB_EVENT_PATH"),
        "GITHUB_API_URL" : os.getenv("GITHUB_API_URL"),

        "GITHUB_TOKEN" : os.getenv("GITHUB_TOKEN"),
        "AUTH_HEADER" : {"Authorization":"Token " + os.getenv("GITHUB_TOKEN")},
        "ALTERNATE_AUTH_HEADER" : {
            "Accept":"application/vnd.github.inertia-preview+json",
            "Authorization":"Token " + os.getenv("GITHUB_TOKEN")
        },
        
        "GITHUB_SHA" : os.getenv("GITHUB_SHA"),
        "PROJECT_BOARD_NAME" : os.getenv("PROJECT_BOARD_NAME", "Automated Board"),
        "GITHUB_REPOSITORY_OWNER" : os.getenv("GITHUB_REPOSITORY").split("/")[0],
        "GITHUB_REPOSITORY_TITLE" : os.getenv("GITHUB_REPOSITORY").split("/")[1],
        "GITHUB_ACTOR" : os.getenv("GITHUB_ACTOR")
    }

    @staticmethod
    def config(name):
        return ENV_VAR.__conf[name]
