#!/bin/bash

# url: https://github.com/travis-ci/travis-ci/issues/4866
# 
source ~/2016_ENSG_PYTHON_COURS/.tox/py32/bin/activate

pip uninstall coverage

pip install 'coverage<4'

# url: https://virtualenv.pypa.io/en/stable/userguide/
deactivate
