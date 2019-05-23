FROM python:3.7.1-stretch

RUN python --version
RUN pip --version
RUN pip install --upgrade pip

RUN pip install coverage
RUN coverage --version

COPY . /cli-test
WORKDIR /cli-test

RUN pip install -r requirements.txt
RUN python runtests.py
