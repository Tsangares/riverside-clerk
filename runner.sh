# Script to run docker command
DOCKER_IMAGE=clerk
LOCAL_PATH_TO_DATA=/Users/jeffreyborowitz/riverside-clerk
docker run -i -t -v $LOCAL_PATH_TO_DATA/data/:/data/ --rm $DOCKER_IMAGE crawl /data/casenumbers.csv
