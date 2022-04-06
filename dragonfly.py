from flask import Flask
from commit_analysis import analysis

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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
