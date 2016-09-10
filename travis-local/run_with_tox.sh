#!/bin/bash
docker	run -it --rm \
		--name docker_travis_tox \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py26:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py26 \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py27:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py27 \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py32:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py32 \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py33:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py33 \
		-v /d/__DATAS__/__DEV__/OSGEO4W/__COURS__/.tox/py34:/home/travis/2016_ENSG_PYTHON_COURS/.tox/py34 \
		travislocal/ensg \
		/bin/bash
		# /home/travis/.local/bin/tox


