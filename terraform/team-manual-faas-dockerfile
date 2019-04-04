FROM: amazonlinux:latest
RUN: yum update -y && \
yum install -y gcc-c++ patch readline readline-devel zlib zlib-devel \
libyaml-devel libffi-devel openssl-devel make bzip2 autoconf automake \
libtool bison iconv-devel sqlite-develnodejs python3 python3-pip python3-devel \
git make zip ruby-devel ruby && \
python3 -m pip install --upgrade pip && \
python3 -m pip install tox
