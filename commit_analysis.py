import os
import json
from github import Github, GithubIntegration
import matplotlib
from matplotlib.figure import Figure

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

def create_chart():
    data = analysis()

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
    
    ax1.pie(fixes, labels=files, autopct='%1.1f%%', shadow=True, radius=1.5, textprops={'fontsize': fontsize}, labeldistance=1.06, pctdistance=0.80)
    wedges = [patch for patch in ax1.patches if isinstance(patch, matplotlib.patches.Wedge)]
    for w in wedges:
        w.set_linewidth = 2
        w.set_edgecolor("black")

    ax1.axis('equal')
    
    dpi = 200
    width = 1920
    height = 1080
    fig1.set_size_inches(width / dpi, height / dpi)

    return fig1

def is_keyword(msg):
    keywords = ['fix', 'bug', 'issue']
    if any(keyword in msg.lower() for keyword in keywords):
        return True
    return False
