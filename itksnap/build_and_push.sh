
#docker build -f Dockerfile.x11vnc -t x11vnc .
#docker tag x11vnc itksnap
docker build -f Dockerfile.turbovnc -t turbovnc .
docker tag turbovnc itksnap
#docker tag turbovnc pangyuteng/theonemule-turbovnc:latest
#docker push pangyuteng/theonemule-turbovnc:latest