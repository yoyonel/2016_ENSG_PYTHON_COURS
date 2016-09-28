#!/bin/bash
docker-compose build && docker-compose run tox tox -e py26
