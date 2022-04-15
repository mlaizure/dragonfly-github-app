import json
from flask import (
    Response, Flask, jsonify, send_from_directory,
    render_template, redirect, url_for
)
from flask_dance.contrib.github import make_github_blueprint, github
from commit_analysis import (
    analysis, create_chart, git_integration, installation
)
from io import BytesIO
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from dotenv import load_dotenv
import os
from github import Github

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


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    user_connection = Github(github.token["access_token"])
    return analysis(installation(user_connection))


@app.route("/chart")
def chart():
    user_connection = Github(github.token["access_token"])
    fig = create_chart(installation(user_connection))
    buf = BytesIO()
    FigureCanvas(fig).print_png(buf)
    return Response(buf.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
