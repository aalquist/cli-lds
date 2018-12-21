FROM python:alpine3.7
COPY . /cli-test
WORKDIR /cli-test

RUN pip install -r requirements.txt
RUN python3 -m unittest discover -s tests -p "test_*"

CMD  python3 bin/akamai-lds
