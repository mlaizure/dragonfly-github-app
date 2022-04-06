import os
import json
from github import Github, GithubIntegration

app_id = '187180'

with open(
        os.path.normpath(os.path.expanduser('./dragonfly-analytics.2022-04-05.private-key.pem')),
        'r'
) as cert_file:
    app_key = cert_file.read()


git_integration = GithubIntegration(
    app_id,
    app_key,
)


def analysis():
    OWNER="mlaizure"
    REPO="holbertonschool-web_react"

    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(OWNER, REPO).id
        ).token
    )
    repo = git_connection.get_repo(f"{OWNER}/{REPO}")

    gh_commits = repo.get_commits("main")

    num_fixes_by_file = {}
    for gh_commit in gh_commits:
        if is_keyword(gh_commit.commit.message):
            for f in gh_commit.files:
                if f.filename in num_fixes_by_file.keys():
                    num_fixes_by_file[f.filename] += 1
                else:
                    num_fixes_by_file[f.filename] = 1
    #print(json.dumps(num_fixes_by_file, indent=4, sort_keys=True))
    return num_fixes_by_file

def is_keyword(msg):
    keywords = ['fix', 'bug', 'issue']
    if any(keyword in msg.lower() for keyword in keywords):
        return True
    return False
