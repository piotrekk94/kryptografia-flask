from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return open("index.html").read()

@app.route('/data', methods=['GET'])
def handle_data():
    number = request.args.get('size')
    def generate():
        xd = open("/dev/rng-tester", "rb")
        for i in range(0, int(int(number)/8192)):
            yield xd.read(8192)
    return Response(generate(), mimetype='application/octet-stream')

app.run(host="0.0.0.0")
