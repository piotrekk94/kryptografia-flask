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
    absd = []
    for dir in os.listdir('./results'):
        absdir = os.path.abspath('results/' + dir)
        absd.append(absdir)
        if os.path.isdir(absdir):
            if path.exists(absdir + "/results.txt") and path.exists(absdir + "/stats.txt"):
                data.append((dir, open(absdir + "/stats.txt").read(), open(absdir + "/results.txt").read()))
    data.append(("Summary", open('./results/freq.txt').read(), open('./results/finalAnalysisReport.txt').read()))
    return render_template('index.html', dataServer=data, temp=absd)

@app.route('/data', methods=['GET'])
def handle_data():
    number = request.args.get('size')
    button = request.args.get('button')
    if button.lower() == 'download':
        return download(number)
    return refresh(number)

def download(size):
    def generate():
        xd = open("/dev/rng-tester", "rb")
        for i in range(0, int(int(size)/8192)):
            yield xd.read(8192)
    return Response(generate(), mimetype='application/octet-stream')

@app.route('/refresh', methods=['GET'])
def refresh(size):
    print(os.system('sh run-tests.sh ' + size))
    return redirect('/')


app.run(host="0.0.0.0")
