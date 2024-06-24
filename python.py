from flask import Flask, render_template, request, Response, jsonify
from graham import *
from kps import *
from jarvis import *

app = Flask(__name__, template_folder="public")


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # retrieve the data sent from JavaScript
    # process the data using Python code
    result = data['value']
    # return the result to JavaScript
    return jsonify({'val': kps(result)})


@app.route('/process2', methods=['POST'])
def process2():
    data = request.get_json()  # retrieve the data sent from JavaScript
    # process the data using Python code
    result = data['value']
    # return the result to JavaScript
    return jsonify({'val': Jarvis(result)})


if __name__ == '__main__':
    app.run(debug=True  , host="0.0.0.0")
