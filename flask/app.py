import subprocess
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    app.logger.info("ok")
    return render_template("index.html")

@app.route('/clicked',methods=["POST"])
def clicked():
    app.logger.info("clicked-docker-ps")
    process = subprocess.Popen(['docker', 'ps'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    return f"<pre>{out}</pre>"
