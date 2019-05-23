#!/bin/bash
echo "building and testing code in python 3 image"

commitId=$(git log -1 --pretty=%H)
echo "$commitId for docker tag"
NAME=akamai-lds
DOCKERNAME="aaalquis/$NAME"
echo $DOCKERNAME
docker build -t $DOCKERNAME:$commitId .

docker build --tag $NAME . 
#docker run -v $(pwd):/cli-test --rm $NAME  python3 runtests.py
#echo "docker run -v $(pwd):/cli-test --rm $NAME  /bin/bash"

docker run -v $(pwd):/cli-test --rm $NAME python3 runtests.py
docker run -v $(pwd):/cli-test --rm $NAME akamai lds help
docker run -v $(pwd):/cli-test --rm $NAME akamai lds help list

cat bin/$NAME | docker run --name testpy2$NAME -i --rm python:2.7.15-stretch 

docker rmi $DOCKERNAME:$commitId
