from flask import Flask
app = Flask(__name__)

@app.route("/testing")
def testing():
    return {"testing": ["test1", "test2", "test3"]}

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
