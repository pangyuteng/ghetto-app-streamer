docker build -f Dockerfile.turbovnc -t turbovnc .
docker tag turbovnc pangyuteng/theonemule-turbovnc:latest
docker push pangyuteng/theonemule-turbovnc:latest