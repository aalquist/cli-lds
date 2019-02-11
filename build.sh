#!/bin/bash
echo "building and testing code in python 3 image"
#docker build --no-cache --tag cli-lds . && docker run --rm cli-lds python bin/akamai-lds
docker build --tag cli-lds . && docker run --rm cli-lds python bin/akamai-lds 
docker rmi cli-lds

echo "testing python 2 not supported"
namepostfix=$(date +%s | shasum | base64 | head -c 6)
cat bin/akamai-lds | docker run --name testpy2$namepostfix -i --rm python:2.7.15-stretch 
#docker rm testpy2$namepostfix