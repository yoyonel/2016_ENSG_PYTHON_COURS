#!/bin/bash
find . -type f -exec dos2unix -k -s -o {} ';'
