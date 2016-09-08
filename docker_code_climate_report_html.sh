#!/bin/bash

echo "launch code climate report (with docker)"

CC_FILENAME_EXPORT=htmlcov/report_codeclimat.html

docker run	\
		--interactive --tty --rm   --env CODECLIMATE_CODE=/home/latty/link_dir/2016_ENSG_PYTHON_COURS	\
		--volume /home/latty/link_dir/2016_ENSG_PYTHON_COURS:/code   --volume /var/run/docker.sock:/var/run/docker.sock   \
		--volume /tmp/cc:/tmp/cc   codeclimate/codeclimate analyze -f html > $CC_FILENAME_EXPORT

echo generate HTML report in: $CC_FILENAME_EXPORT

# on lance le webbroswer cli lynx pour visualier le report HTML
lynx $CC_FILENAME_EXPORT