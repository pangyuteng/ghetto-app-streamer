
#docker build -f Dockerfile.x11vnc -t x11vnc .
docker build -f Dockerfile.turbovnc -t turbovnc .
docker tag turbovnc pangyuteng/turbovnc:itksnap
docker push pangyuteng/turbovnc:itksnap

docker build -f Dockerfile.turbovnc.glxgears -t glxgears .
docker tag glxgears pangyuteng/turbovnc:glxgears
docker push pangyuteng/turbovnc:glxgears

