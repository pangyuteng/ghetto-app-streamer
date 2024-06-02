"""
  upstream app {
    server app:3000;
  }
location /app {
    proxy_pass http://app;
}
"""

NGINX_TEMPLATE="""
events {}

http {  
  upstream serv {
    server flask:5000;
  }
  server {
    listen 80;
    location / {
      proxy_pass http://serv;
    }
  }

}
"""
import os
import subprocess
from flask import Flask, render_template, jsonify

app = Flask(__name__)

NGINX_PATH = "/share/nginx.conf"
if not os.path.exists(NGINX_PATH):
    with open(NGINX_PATH,'w') as f:
        f.write(NGINX_TEMPLATE)

@app.route('/')
def hello():
    app.logger.info("home...")
    return render_template("index.html")

@app.route('/clicked',methods=["POST"])
def clicked():
    app.logger.info("clicked...")
    process = subprocess.Popen(['docker', 'ps'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    return jsonify({"stdout":out,"stderr":err})

@app.route('/reload-nginx',methods=["POST"])
def reload_nginx():
    app.logger.info("reload-nginx...")
    cmd_list = 'docker exec ghetto-app-streamer-nginx-1 /usr/sbin/nginx -s reload'.split(' ')
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    return jsonify({"stdout":out,"stderr":err})
    
