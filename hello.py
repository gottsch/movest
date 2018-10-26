from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/overview/<name>")
def overview(name):
    x = request.args.get('x')
    #return "Overview"
    return render_template('overview.html', name=name + ":" + x)

if __name__ == "__main__":
    app.run(debug=True)