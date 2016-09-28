#!/bin/bash
docker-compose build
# docker-compose run tox tox -e py27
# winpty docker-compose run tox tox -e py27
docker-compose run -d tox tox -e py27