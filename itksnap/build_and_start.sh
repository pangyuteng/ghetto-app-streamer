docker build -t ok-turbovnc -f Dockerfile.workspace .

docker run -it -v /mnt:/mnt -p 80:80 ok-turbovnc