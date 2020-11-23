docker stop nvr_erudite
docker rm nvr_erudite
docker build -t nvr_erudite .
docker run -d \
 -it \
 --restart on-failure \
 --name nvr_erudite \
 --net=host \
 -p 6000:6000 \
 nvr_erudite
