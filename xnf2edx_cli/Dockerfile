FROM python:3.10.10-bullseye
MAINTAINER Sergio Puche García <spuche@upv.es>

RUN apt-get update
RUN /bin/bash -c 'apt-get upgrade -y'

# Install the project
RUN /bin/bash -c "git clone https://git.upv.es/serpucga/xnf2edx_cli.git"
WORKDIR "xnf2edx_cli"
RUN /bin/bash -c "python -m pip install -r requirements/prod.txt"
