FROM amazonlinux:latest
COPY firebreak-q1-faas-git/requirements.txt ./
RUN yum update -y && \
yum install -y python3 python3-pip python3-devel git make zip libffi-devel openssl-devel
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install tox
