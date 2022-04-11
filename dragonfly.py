from flask import Response, Flask, jsonify, send_from_directory, render_template
from commit_analysis import analysis, create_chart
from io import BytesIO
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__,
            template_folder="frontend/build",
            static_url_path="",
            static_folder="frontend/build")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route("/testing")
def testing():
    fig = create_chart()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return 'data:image/png;base64,{data}'
    return Response(buf, mimetype="application/png")

@app.route("/")
def index():
    return render_template("index.html")

#@app.route("/static/js/<path:path>")
#def build(path):
#    return send_from_directory("./frontend/build/static/js", path)

@app.route("/dashboard")
def dashboard():
    return analysis()

@app.route("/chart")
def chart():
    fig = create_chart()
    buf = BytesIO()
    # fig.savefig(buf, format="png")
    FigureCanvas(fig).print_png(buf)
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/>"
    return Response(buf.getvalue(), mimetype="image/png")
    # return Response(buf, mimetype="image/png")
    # return buf

if __name__ == "__main__":
    app.run(host='0.0.0.0')
