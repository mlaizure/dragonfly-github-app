import os
import json
from github import Github, GithubIntegration, Installation
import matplotlib
from matplotlib.figure import Figure
import requests

app_id = 187180

if os.getenv("PRIVATE_KEY"):
    app_key = os.getenv("PRIVATE_KEY")

else:
    with open(
            os.path.normpath(os.path.expanduser(
                './dragonfly-analytics.2022-04-05.private-key.pem')),
            'r'
    ) as cert_file:
        app_key = cert_file.read()


git_integration = GithubIntegration(
    app_id,
    app_key,
)


def get_repos(inst_id, user_connection):
    """getting list of repos from user's installation"""
    repos_response = user_connection.get(
        f"/user/installations/{inst_id}/repositories")
    repos_response_dict = repos_response.json()
    repos = repos_response_dict["repositories"]
    return repos


def get_installation_id(user_connection):
    """finding user's installation id via flask_dance connection"""
    installations = user_connection.get(
        "/user/installations"
    ).json()["installations"]

    user = user_connection.get("/user").json()

    installations = [
        inst for inst in installations if
        inst["app_id"] == app_id
        and inst["account"]["login"] == user["login"]
    ]
    if len(installations) > 0:
        return installations[0]["id"]
    else:
        return None


def analysis(inst_id, user_connection, owner, repo_name):
    """uses PyGithub connection to compile relevant commit info"""
    git_connection = Github(login_or_token=git_integration.get_access_token(
        inst_id).token)

    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    branches = repo.get_branches()
    branch_names = [branch.name for branch in branches]
    if "main" in branch_names:
        main_branch = "main"
    elif "master" in branch_names:
        main_branch = "master"

    gh_commits = repo.get_commits(main_branch)

    num_fixes_by_file = {}
    for gh_commit in gh_commits:
        if is_keyword(gh_commit.commit.message):
            for f in gh_commit.files:
                if not is_ignored(f.filename):
                    if f.filename in num_fixes_by_file.keys():
                        num_fixes_by_file[f.filename] += 1
                    else:
                        num_fixes_by_file[f.filename] = 1
    return num_fixes_by_file


def is_keyword(msg):
    """checking if keyword in commit message"""
    keywords = ['fix', 'bug', 'issue']
    if any(keyword in msg.lower() for keyword in keywords):
        return True
    return False


def is_ignored(path):
    """filtering some non-code file extensions"""
    ignore_ext = ['.json', '.md', '.ps', '.eps', '.txt', '.xml', '.xsl',
                  '.rss', '.xslt', '.xsd', '.wsdl', '.wsf', '.yaml', '.yml',
                  '~', '#', '.png', '.jpg', '.jpeg', '.gif']
    for ext in ignore_ext:
        length = len(ext)
        if path[-length:] == ext:
            return True
    return False


def create_chart(inst_id, user_connection, owner, repo_name):
    """creating pie chart with Matplotlib"""
    data = analysis(inst_id, user_connection, owner, repo_name)

    files = []
    fixes = []

    for k, v in data.items():
        files.append(k.split('/')[-1])
        fixes.append(v)
    fig1 = Figure()
    ax1 = fig1.subplots()
    if len(files) > 10:
        fontsize = 10
    else:
        fontsize = 15

    ax1.pie(fixes, labels=files, autopct='%1.1f%%', shadow=True,
            radius=1.5, textprops={'fontsize': fontsize},
            labeldistance=1.06, pctdistance=0.80)
    wedges = [patch for patch in ax1.patches if isinstance(
        patch, matplotlib.patches.Wedge)]
    for w in wedges:
        w.set_linewidth = 2
        w.set_edgecolor("black")

    ax1.axis('equal')

    dpi = 200
    width = 1920
    height = 1080
    fig1.set_size_inches(width / dpi, height / dpi)

    return fig1
