#!/bin/bash
#
# urls: 
# - https://docs.docker.com/engine/tutorials/dockervolumes/
# - https://docs.docker.com/engine/reference/commandline/volume_inspect/
# - https://docs.docker.com/engine/reference/commandline/volume_ls/
# - https://forums.docker.com/t/volume-mounts-in-windows-does-not-work/10693/5
docker	run -it --rm \
		--name docker_travis_tox \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py26:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py26 \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py27:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py27 \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py32:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py32 \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py33:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py33 \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py34:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py34 \
		travislocal/ensg \
		/bin/bash
