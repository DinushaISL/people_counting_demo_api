from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def start():
    return "started"


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=7788)
