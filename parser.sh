# Script to run docker command
DOCKER_IMAGE=clerk
# Go to the directory where you clone the project and do:
# docker build -t clerk .
LOCAL_PATH_TO_DATA=/home/ec2-user/riverside-clerk
# Change this directory to match where your vesion of input data are

docker run -i -t -v $LOCAL_PATH_TO_DATA/conf.env:/opt/conf.env -v $LOCAL_PATH_TO_DATA/data/:/data/ --rm $DOCKER_IMAGE parse  --filename /data/output/ --output /data/parsed.csv
