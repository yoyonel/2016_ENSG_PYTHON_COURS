#!/bin/bash
# url: http://stackoverflow.com/questions/14372645/convert-dos2unix-line-endings-for-all-files-in-a-directory
find . -type f -exec dos2unix -k -s -o {} ';'
