FROM centos:7
MAINTAINER "Edson Yamada" <enyamada@gmail.com>

RUN rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm

RUN yum install -y \
          gcc \
          mysql-devel \
          MySQL-python \
          python-pip 

RUN pip install  \
          Flask \
          pyyaml \
          retrying

EXPOSE 5000

WORKDIR /root
ADD config.yml config.yml
ADD *.py /root/
CMD python steps.py 
