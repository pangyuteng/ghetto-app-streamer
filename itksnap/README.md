```
ref 

https://github.com/theasp/docker-novnc

coool
https://www.youtube.com/watch?v=L4nqky8qGm8
https://github.com/theonemule/docker-opengl-turbovnc


docker run -it -u $(id -u):$(id -g) -v /mnt:/mnt -p 80:80 turbovnc



EVEN COOLER. virtualgl headless gpu

export DISPLAY=:1
vglrun -d :1 glxgears
/opt/VirtualGL/bin/glxinfo -display :1 | grep vendor

https://github.com/didzis/nvidia-xorg-virtualgl-docker
https://github.com/VirtualGL/virtualgl/issues/10
https://github.com/dcommander/virtualgl_docker_examples
https://virtualgl.org/Documentation/HeadlessNV
```
