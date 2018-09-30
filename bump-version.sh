#!/bin/bash

# Use this bash script to set Version information in all file locations. IE: setup.py


if [ $# -ne 1 ]; then
   echo "usage: bump-version.sh VERSION"
   exit 1
fi

# setup.py

FILE=$PWD/setup.py

if [ ! -e $FILE ]; then
   echo "error: setup.py not found. aborting."
   exit 1
fi

# setup.py
sed -i "s/^__VERSION__.*/__VERSION__ = \"$1\"/g" $FILE

