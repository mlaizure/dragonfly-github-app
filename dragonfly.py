from flask import Flask
from commit_analysis import analysis, create_chart
from io import BytesIO
import base64
from matplotlib.figure import Figure

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route("/testing")
def testing():
    return {"testing": ["test1", "test2", "test3"]}

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/dashboard")
def dashboard():
    return analysis()

@app.route("/chart")
def chart():
    fig = create_chart()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
