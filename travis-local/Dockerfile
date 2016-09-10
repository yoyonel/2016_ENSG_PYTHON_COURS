FROM quay.io/travisci/travis-python:latest

RUN pip install --upgrade pip

USER travis

WORKDIR /home/travis

RUN git clone https://github.com/yoyonel/2016_ENSG_PYTHON_COURS &&\
	cd 2016_ENSG_PYTHON_COURS && \
	git checkout dev-travis-local

WORKDIR 2016_ENSG_PYTHON_COURS

RUN pip install --user tox coveralls codeclimate-test-reporter

# url: https://github.com/docker/docker/issues/684
ENV PATH /home/travis/.local/bin:$PATH

COPY tox.ini /home/travis/2016_ENSG_PYTHON_COURS/tox.ini

# For sharing volumes
RUN mkdir -p /home/travis/2016_ENSG_PYTHON_COURS/.tox/py26 &&\
	mkdir -p /home/travis/2016_ENSG_PYTHON_COURS/.tox/py27 &&\
	mkdir -p /home/travis/2016_ENSG_PYTHON_COURS/.tox/py32 &&\
	mkdir -p /home/travis/2016_ENSG_PYTHON_COURS/.tox/py33 &&\
	mkdir -p /home/travis/2016_ENSG_PYTHON_COURS/.tox/py34

COPY downgrade_coverage_for_py32.sh /home/travis/2016_ENSG_PYTHON_COURS/
RUN sudo chown travis:travis downgrade_coverage_for_py32.sh
RUN sudo apt-get  install -y dos2unix
RUN dos2unix downgrade_coverage_for_py32.sh

# # ENTRYPOINT
# COPY entry_point.sh /entry_point.sh

# RUN sudo apt-get  install -y dos2unix
# RUN sudo dos2unix /entry_point.sh

# ENTRYPOINT ["/entry_point.sh"]
