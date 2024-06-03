NGINX_TEMPLATE="""
events {
}

http {  

  server {
    listen 80 default_server;
    location / {
      proxy_pass http://flask:5000/;
    }
    {% for item in container_list %}
    location /{{item.container_name}}/ok/ {
      proxy_pass http://{{item.container_name}}:8080/;
      proxy_buffering off;
    }
    location /novnc/{{item.container_name}}/websockify {
      proxy_pass http://{{item.container_name}}:8080/;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      proxy_set_header Host $host;
      proxy_read_timeout 61s;
      proxy_buffering off;
    }
    {% endfor %}
  }

}
"""

import os
import traceback
import subprocess
import uuid
from flask import Flask, render_template, jsonify
from jinja2 import Environment

app = Flask(__name__)

NGINX_PATH = "/share/nginx.conf"

container_list = []
@app.route('/')
def hello():
    global container_list
    app.logger.info("home...")
    return render_template("index.html",container_list=container_list)

@app.route('/add-novnc',methods=["POST"])
def add_novnc():
    global container_list
    try:
        app.logger.info("add_novnc...")
        container_name = f'novnc-{str(uuid.uuid4())}'
        cmd_list = f'docker run -d --network=ghetto-app-streamer_appstream --expose=8080 --name={container_name} pangyuteng/docker-novnc:latest'.split(' ')
        process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        container_uid = out.decode("utf-8")
        err = err.decode("utf-8")
        container_list.append(dict(
            container_name=container_name,
            container_uid=container_uid,
        ))
        cmd_list = f'docker ps'.split(' ')
        process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return jsonify({"stdout":out,"stderr":err})
    except:
        return jsonify(traceback.format_exc())
@app.route('/reload-nginx',methods=["POST"])
def reload_nginx():
    global container_list
    try:
        app.logger.info("reload-nginx...")
        with open(NGINX_PATH,'w') as f:
            content = Environment().from_string(NGINX_TEMPLATE).render(container_list=container_list)
            f.write(content)
        cmd_list = 'docker exec ghetto-app-streamer-nginx-1 /usr/sbin/nginx -s reload'.split(' ')
        process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        out = out.decode("utf-8")
        err = err.decode("utf-8")
        return jsonify({"stdout":out,"stderr":err})
    
    except:
        return jsonify(traceback.format_exc())