NGINX_TEMPLATE="""
events {
}

http {  

  server {
    listen 80 default_server;
    location / {
      proxy_pass http://flask:5000/;
    }
    {% for _,item in container_dict.items() %}
    location /novnc/{{item.container_name}}/ {
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
import json
from flask import Flask, render_template, jsonify, request
from jinja2 import Environment

app = Flask(__name__)

NGINX_PATH = "/share/nginx.conf"

def get_container_dict():
    
    container_dict = {}

    cmd_list = f'docker ps --format json'.split(' ')
    app.logger.info(cmd_list)
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    out_list = out.split('\n')
    err = err.decode("utf-8")
    if len(err) > 0:
        raise ValueError(err)

    for item in out_list:
        if len(item) == 0:
            continue
        item = json.loads(item)
        container_name = item.get("Names")
        if container_name.startswith("novnc-"):
            item = dict(item)
            item["container_name"]=container_name
            app.logger.info(str(item))
            container_dict[container_name]=item

    with open(NGINX_PATH,'w') as f:
        content = Environment().from_string(NGINX_TEMPLATE).render(container_dict=container_dict)
        f.write(content)

    cmd_list = 'docker exec ghetto-app-streamer-nginx-1 /usr/sbin/nginx -s reload'.split(' ')
    app.logger.info(cmd_list)
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    if "signal process started" in err:
        err = ""
    if len(err) > 0:
        raise ValueError(err)
    return container_dict
    
def start_container(username):
    container_name = f'novnc-{username}'
    cmd_list = f'docker run -d --network=ghetto-app-streamer_appstream --expose=8080 --name={container_name} pangyuteng/docker-novnc:latest'.split(' ')
    app.logger.info(cmd_list)
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    if len(err) > 0:
        raise ValueError(err)


def remove_container(username):
    container_name = f'novnc-{username}'
    cmd_list = f'docker stop {container_name}'.split(' ')
    app.logger.info(cmd_list)
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    if len(err) > 0:
        raise ValueError(err)
    cmd_list = f'docker rm {container_name}'.split(' ')
    app.logger.info(cmd_list)
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    if len(err) > 0:
        raise ValueError(err)


with open(NGINX_PATH,'w') as f:
    content = Environment().from_string(NGINX_TEMPLATE).render(container_dict=get_container_dict())
    f.write(content)

@app.route('/')
def hello():
    app.logger.info("home...")
    return render_template("index.html")

@app.route('/status',methods=["GET"])
def status():
    app.logger.info("status...")
    err_list = []
    try:
        container_dict = get_container_dict()
        return render_template("response.html",
            container_dict=container_dict,
        )
    except:
        err_list.append(traceback.format_exc())
        return render_template("response.html",err_list=err_list,container_dict={})

@app.route('/add-novnc',methods=["POST"])
def add_novnc():
    err_list = []
    try:
        app.logger.info("add_novnc...")
        username = request.get_json().get('username',None)
        if username is None:
            username = str(uuid.uuid4()).split('-')[-1]

        start_container(username)
        
        container_dict = get_container_dict()

        return render_template("response.html",
            container_dict=container_dict,
            err_list=err_list,
        )
    except:
        err_list.append(traceback.format_exc())
        return render_template("response.html",err_list=err_list,container_dict={})

@app.route('/delete-novnc',methods=["POST"])
def delete_novnc():
    err_list = []
    try:
        app.logger.info("delete-novnc...")
        username = request.get_json().get('username',None)
        if username is None:
            raise ValueError("username is None")

        remove_container(username)
        container_dict = get_container_dict()
        return render_template("response.html",
            container_dict=container_dict,
            err_list=err_list,
        )
        return render_template("response.html",err_list=err_list)
    except:
        err_list.append(traceback.format_exc())
        return render_template("response.html",err_list=err_list,container_dict={})