import json
from flask import (
    Response, Flask, jsonify, send_from_directory,
    render_template, redirect, url_for, request, session
)
from flask_dance.contrib.github import make_github_blueprint, github
from commit_analysis import (
    analysis, create_chart, get_repos, get_installation_id
)
from io import BytesIO
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from dotenv import load_dotenv
import os
from github import Github
from datetime import timedelta

load_dotenv()

app_id = 187180

app = Flask(__name__,
            template_folder="build",
            static_url_path="",
            static_folder="build")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get(
    "GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)


@app.route("/user-is-authenticated")
def user_is_authenticated():
    return {
        "userIsAuthenticated": github.authorized,
        "redirectUrl": url_for("github.login")
    }


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    owner = request.args.get('owner')
    repo_name = request.args.get('repo_name')
    inst_id = get_installation_id(github)
    if not inst_id:
        return { "userHasNoInstallation": True }
    else:
        r = analysis(inst_id, github, owner, repo_name)
        if len(r) == 0:
            return { "repositoryHasNoCommits": True}
        else:
            return r


@app.route("/chart")
def chart():
    owner = request.args.get('owner')
    repo_name = request.args.get('repo_name')
    inst_id = get_installation_id(github)
    if not inst_id:
        return { "userHasNoInstallation": true }
    else:
        fig = create_chart(inst_id, github, owner, repo_name)
        buf = BytesIO()
        FigureCanvas(fig).print_png(buf)
        return Response(buf.getvalue(), mimetype="image/png")


@app.route("/repos")
def repos():
    inst_id = get_installation_id(github)
    if not inst_id:
        return { "userHasNoInstallation": True }
    else:
        return {"repos": get_repos(inst_id, github)}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
