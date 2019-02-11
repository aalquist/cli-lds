FROM python:3.7.1-stretch
COPY . /cli-test
WORKDIR /cli-test

RUN python --version
RUN pip --version
RUN pip install --upgrade pip

RUN pip install coverage
RUN coverage --version

RUN pip install -r requirements.txt

RUN python runtests.py

CMD  python3 bin/akamai-lds
