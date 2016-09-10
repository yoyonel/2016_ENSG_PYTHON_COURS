FROM quay.io/travisci/travis-python:latest

USER travis

WORKDIR /home/travis

RUN git clone https://github.com/yoyonel/2016_ENSG_PYTHON_COURS

WORKDIR 2016_ENSG_PYTHON_COURS

RUN pip install --user tox coveralls codeclimate-test-reporter

RUN export PATH=$PATH:~/.local/bin

# RUN cd /home/travis/2016_ENSG_PYTHON_COURS && \
	# ~/.local/bin/tox
# RUN tox

# # ENTRYPOINT
# COPY entry_point.sh /entry_point.sh

# RUN sudo apt-get  install -y dos2unix
# RUN sudo dos2unix /entry_point.sh

# ENTRYPOINT ["/entry_point.sh"]
