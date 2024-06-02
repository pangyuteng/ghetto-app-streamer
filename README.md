# ghetto-app-streamer


docker build -t firefox .
docker run --rm -it -p 3000:3000 firefox bash

## ref novnc

https://stackoverflow.com/questions/16296753/can-you-run-gui-applications-in-a-linux-docker-container
https://www.server-world.info/en/note?os=Ubuntu_22.04&p=desktop&f=8

https://github.com/ConSol/docker-headless-vnc-container/blob/master/kubernetes/README.md

docker run -p 5901:5901 -p 6901:6901 consol/debian-icewm-vnc # just works, icewm ugly af
no-copy-paste? https://github.com/ConSol/docker-headless-vnc-container/issues/194

https://github.com/kasmtech/noVNC/

## ref reverse proxy

https://serverfault.com/a/708779

docker exec -it ghetto-app-streamer-flask-1 bash
docker exec ghetto-app-streamer-nginx-1 /usr/sbin/nginx -s reload

https://datawookie.dev/blog/2021/08/websockify-novnc-behind-an-nginx-proxy

https://hub.docker.com/r/x11docker/xfce


## todos

[x] create/find-existing Dockerfile.novnc for app streamer

    + play 4k youtube video in browser to test frame rate
    + can copy paste, key-combo-shortcuts

    use below for streaming desktop
    https://github.com/linuxserver/docker-baseimage-kasmvnc

[x] above example already shows you how to install shit.

[ ] flask/nginx to spin up docker to do reverse proxy

[ ] deploy via k8s/swarm


```
