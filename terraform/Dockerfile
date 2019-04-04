FROM amazonlinux:latest
RUN yum update -y && \
yum install -y gpg gcc gcc-c++ patch readline readline-devel zlib zlib-devel \
libyaml-devel libffi-devel openssl-devel curl which make bzip2 autoconf automake \
libtool bison iconv-devel sqlite-develnodejs python3 python3-pip python3-devel \
git make zip bash && \
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB && \
curl -sSL https://get.rvm.io | bash -s stable && \
useradd -G rvm root && \
source /etc/profile.d/rvm.sh && \
rvm install 2.6.2 && \
rvm use 2.6.2 --default && \
python3 -m pip install --upgrade pip && \
python3 -m pip install tox
