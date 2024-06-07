# python-integration-testing
all python integration testings


# build the docker image without cache
docker-compose -f docker-compose.yml -f tests/docker-compose.yml build --no-cache 

# bring up the entire fleet of docker images
docker-compose -f docker-compose.yml -f tests/docker-compose.yml  up -d

# bring down the entire fleet of docker images
docker-compose -f docker-compose.yml -f tests/docker-compose.yml  down

