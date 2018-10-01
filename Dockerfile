FROM debian:jessie-slim
LABEL maintainer="Benjamin MABILLE <benjy80@gmail.com"

RUN apt-get -y update \
	&& apt-get install --no-install-recommends -y python3 python3-dev python3-pip build-essential kmod fuse config-package-dev apt-utils tree devscripts lintian \
	&& rm -rf /var/lib/apt/lists/* \
	&& mkdir /shared

COPY . /shared/

RUN python3 -m pip install pip setuptools virtualenv --upgrade && \
	mkdir -p /mnt/apps/ && \
    virtualenv -p $(which python3) /mnt/apps/pyfuse && \
    echo "source /mnt/apps/pyfuse/bin/activate" >> /root/.bashrc

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh

VOLUME ["/shared"]
WORKDIR /shared

EXPOSE 5555