NGINX_TEMPLATE="""
events {
}

http {  

  server {
    listen 80 default_server;
    location / {
      proxy_pass http://flask:5000/;
    }
    {% for _,item in containers_dict.items() %}
    location /novnc/{{item.container_name}}/ {
      proxy_pass http://{{item.container_name}}:8888/;
      proxy_buffering off;
    }
    location /novnc/{{item.container_name}}/websockify {
      proxy_pass http://{{item.container_name}}:8888/;
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
import time
import hashlib
import traceback
import subprocess
import uuid
import json
import requests
from flask import Flask, render_template, jsonify, request
from jinja2 import Environment

app = Flask(__name__)

NGINX_PATH = "/share/nginx.conf"

def get_containers_dict():
    
    containers_dict = {}

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
        if container_name.startswith(CONTAINER_PREFIX):
            item = dict(item)
            item["container_name"]=container_name
            item["url"]= f"novnc/{container_name}/vnc.html?resize=remote&path=novnc/{container_name}/websockify"
            app.logger.info(str(item))
            containers_dict[container_name]=item

    with open(NGINX_PATH,'w') as f:
        content = Environment().from_string(NGINX_TEMPLATE).render(containers_dict=containers_dict)
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
    return containers_dict

DOCKER_CONTAINER_NAME = "itksnap"
CONTAINER_PREFIX = "itksnap-"
def get_container_name(username):
    m = hashlib.sha256()
    m.update(username.encode("utf-8"))
    return f'{CONTAINER_PREFIX}{m.digest().hex()[:8]}'

def container_exists(username):
    container_name = get_container_name(username)
    return container_name in get_containers_dict().keys()

def start_container(username,workspace_path):
    container_name = get_container_name(username)
    cmd_list = f'docker run -d --network=ghetto-app-streamer_appstream -v /mnt/hd1/github/ghetto-app-streamer/share:/mnt/share -e WORKSPACE_PATH={workspace_path} --expose=8888 --name={container_name} {DOCKER_CONTAINER_NAME}'.split(' ')
    app.logger.info(cmd_list)
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    if len(err) > 0:
        raise ValueError(err)

def remove_container(username):
    container_name = get_container_name(username)
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
    content = Environment().from_string(NGINX_TEMPLATE).render(containers_dict=get_containers_dict())
    f.write(content)

@app.route('/')
def hello():
    app.logger.info("home...")
    return render_template("index.html")

@app.route('/itksnap')
def itksnap():
    username = request.args.get('username',None)
    workspace_path = request.args.get('workspace_path',None)
    err_list = []
    container_info = None
    try:
        if username is None or workspace_path is None:
            raise ValueError("missing username or workspace_path params!")
        if container_exists(username):
            #remove_container(username)
            time.sleep(1)
        else:
            start_container(username,workspace_path)
        time.sleep(1)
        containers_dict = get_containers_dict()
        container_name = get_container_name(username)
        container_info = containers_dict[container_name]
        """
        status_code = 'pending'
        counter = 0
        while status_code == "pending" or counter < 3:
            res = requests.get(container_info["url"])
            status = res.status_code
            time.sleep(1)
            counter+=1
        if status_code != 200:
            raise ValueError("trouble loading novnc?")
        """
    except:
        err_list.append(traceback.format_exc())

    return render_template("itksnap.html",
        container_info=container_info,
        username=username,
        workspace_path=workspace_path,
        err_list=err_list)

@app.route('/status',methods=["GET"])
def status():
    app.logger.info("status...")
    err_list = []
    try:
        containers_dict = get_containers_dict()
        return render_template("response.html",
            containers_dict=containers_dict,
        )
    except:
        err_list.append(traceback.format_exc())
        return render_template("response.html",err_list=err_list,containers_dict={})

@app.route('/add-itksnap',methods=["POST"])
def add_itksnap():
    err_list = []
    try:
        app.logger.info("add_itksnap...")
        username = request.get_json().get('username',None)
        workspace_path = request.get_json().get('workspace_path',None)
        if username is None:
            raise ValueError("username not specified!")
        if container_exists(username):
            raise ValueError("container found, please delete container first!")

        start_container(username,workspace_path)
        
        containers_dict = get_containers_dict()

        return render_template("response.html",
            containers_dict=containers_dict,
            err_list=err_list,
        )
    except:
        err_list.append(traceback.format_exc())
        return render_template("response.html",err_list=err_list,containers_dict={})

@app.route('/delete-itksnap',methods=["POST"])
def delete_itksnap():
    err_list = []
    try:
        app.logger.info("delete-itksnap...")
        username = request.get_json().get('username',None)
        if username is None:
            raise ValueError("username is None")

        remove_container(username)
        containers_dict = get_containers_dict()
        return render_template("response.html",
            containers_dict=containers_dict,
            err_list=err_list,
        )
        return render_template("response.html",err_list=err_list)
    except:
        err_list.append(traceback.format_exc())
        return render_template("response.html",err_list=err_list,containers_dict={})