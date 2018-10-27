from flask import Flask
import os
from os import path
from flask import Response
from flask import request
from flask import redirect
from flask import render_template

app = Flask(__name__)
@app.route("/", methods=['GET'])
def hello():
    data = []
    for dir in os.listdir():
        if os.path.isdir(dir):
            if path.exists(dir + "/result.txt") and path.exists(dir + "/stats.txt"):
                data.append((dir, open(dir + "/stats.txt").read(), open(dir + "/result.txt").read()))
    return render_template('index.html', dataServer=data)

@app.route('/data', methods=['GET'])
def handle_data():
    number = request.args.get('size')
    button = request.args.get('button')
    if button == 'download':
        return download(number)
    return refresh()

def download(size):
    def generate():
        xd = open("/dev/rng-tester", "rb")
        for i in range(0, int(int(size)/8192)):
            yield xd.read(8192)
    return Response(generate(), mimetype='application/octet-stream')

@app.route('/refresh', methods=['GET'])
def refresh():
    print(os.system('sh runTests'))
    return redirect('/')


app.run(host="0.0.0.0")
