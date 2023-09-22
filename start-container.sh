# rebuild image
docker rmi -f ibs-container
docker build -t ibs-container .

# stop older containers
docker rm -f ibs

# start new container
docker run -d --restart always --name ibs ibs-container

