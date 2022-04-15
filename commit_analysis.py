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


def getInstallationById(git_integration, installationId):

    token = git_integration.get_access_token(installationId).token

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.machine-man-preview+json",
        "User-Agent": "PyGithub/Python",
    }
    repos_url = f"{git_integration.base_url}/installation/repositories"
    repos_response = requests.get(repos_url, headers=headers)
    repos_response_dict = repos_response.json()
    first_repo = repos_response_dict["repositories"][0]
    owner = first_repo["owner"]["login"]
    repo_name = first_repo["name"]

    return {
        "installation": git_integration.get_installation(owner, repo_name),
        "owner": owner,
        "repo_name": repo_name,
    }


def installation(user_connection):

    installations = user_connection.get_user().get_installations()
    inst = [inst for inst in installations if inst.app_id == app_id][0]

    return getInstallationById(git_integration, inst.id)


def analysis(inst):

    git_connection = Github(login_or_token=git_integration.get_access_token(
        inst["installation"].id).token)

    owner = inst["owner"]
    repo_name = inst["repo_name"]
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    gh_commits = repo.get_commits("master")

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
    keywords = ['fix', 'bug', 'issue']
    if any(keyword in msg.lower() for keyword in keywords):
        return True
    return False


def is_ignored(path):
    ignore_ext = ['.json', '.md', '.ps', '.eps', '.txt', '.xml', '.xsl',
                  '.rss', '.xslt', '.xsd', '.wsdl', '.wsf', '.yaml', '.yml',
                  '~', '#', '.png', '.jpg', '.jpeg', '.gif']
    for ext in ignore_ext:
        l = len(ext)
        if path[-l:] == ext:
            return True
    return False


def create_chart(inst):
    data = analysis(inst)

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
