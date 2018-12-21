#!/bin/bash
echo "building and testing code in python 3 image"
docker build --tag cli-lds . && docker run --rm cli-lds python bin/akamai-lds

echo "testing python 2 not supported"
cat bin/akamai-lds | docker run -i --rm python:2.7.15-stretch 