#!/bin/bash

source ~/2016_ENSG_PYTHON_COURS/.tox/py32/bin/activate

pip uninstall coverage

pip install 'coverage<4'

deactivate
