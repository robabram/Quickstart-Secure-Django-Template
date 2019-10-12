#!/usr/bin/env bash
#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# Project Quickstart Script.
#
# This script will check for project in the current directory, if it does not exist
# it will clone the project from Github. Then it will create a python Virtual
# Environment, update it with the required packages.  Last it will initialize
# a Sqlite3 database and configure Oauth3.  After that it is ready to launch the
# django test server.
#

echo -e "\nLaunching Quickstart Secure Django Template project\n"
echo -e "Note: you may run this as many times as you want, remember to run it from the"
echo -e "      Quickstart-Secure-Django-Template directory after the project has been downloaded.\n"

FNR=0

test_exec () {

    echo -n "info: checking for '$1' executable... "

    EXEC=$(which $1 > /dev/null 2>&1)

    if [ $? -ne 0 ]; then
       echo "not found"
       echo "error: unable to locate '$1' executable, please install '$1' to continue."
       FNR=1
    fi

    echo "found"
    FNR=0
}

test_exec "python3"
if [ $FNR -ne 0 ]; then
   return
fi

test_exec "git"
if [ $FNR -ne 0 ]; then
   return
fi

PYTHON3=$(which "python3")
GIT=$(which "git")

CURDIR=`pwd`
GIT_PROJECT="Quickstart-Secure-Django-Template"

test_project_dir () {

    # test to see if our current directory is the git project directory.
    if [[ "$CURDIR" =~ $GIT_PROJECT ]]; then
        FNR=0
        return
    fi

    # test and see if the project is in a sub-directory.
    SUB_DIR="$CURDIR/$GIT_PROJECT"
    if [ -d $SUB_DIR ]; then
        echo "info: found project in sub-directory, moving to sub-directory."
        cd "$SUB_DIR"
        CURDIR=`pwd`
        echo "$CURDIR"
        FNR=0
        return
    fi

    FNR=1
}

download_project () {

    echo "cloning project..."

    $($GIT clone "https://github.com/robabram/Quickstart-Secure-Django-Template.git")

    if [ $? -ne 0 ]; then
        echo -e "error: failed to download project from github, aborting."
        FNR=1
    fi

    cd "$GIT_PROJECT"
    CURDIR=`pwd`

    FNR=0

}

activate_venv () {

    VENV_DIR="$CURDIR/venv"

    # If the venv directory does not exist, create a new VE.
    if [ ! -d "$VENV_DIR" ]; then
        $PYTHON3 -m venv venv
    fi

    # Activate virtual environment
    source "$CURDIR/venv/bin/activate"

    PIP=$(which "pip")

    # Check that we have updated packages
    PIP_CHECK=$($PIP freeze | grep idna)

    if [[ ! $PIP_CHECK =~ "idna" ]]; then
        echo -e "info: installing required python packages in virtual environment..."
        $PIP install -r requirements.txt > /dev/null 2>&1
    fi

}

# Check and see if the project directory can be found
test_project_dir

if [ $FNR -ne 0 ]; then
    download_project

    # check if cloning the project failed
    if [ $FNR -ne 0 ]; then
        return
    fi
fi

activate_venv

# Set environment required variables
export PYTHONPATH=`pwd`
export DJANGO_SETTINGS_MODULE="django_project.proj.settings.local"

cd django_project

echo -e "info: checking databases have been migrated..."
python3 manage.py migrate

echo -e "info: checking project oauth2 settings..."
python3 manage.py admin --init-oauth

echo -e "info: loading example api data fixture..."
python3 manage.py loaddata apps/api_example/fixtures/testdata.json

echo -e "info: project is ready to run."
echo -e ""
echo -e "info: to launch django server run:"
echo -e "info:    'cd django_project; python3 manage.py runserver'"
echo -e ""
echo -e "info: to launch uwsgi server run:"
echo -e "info:    '/usr/local/Quickstart-Secure-Django-Template/venv/bin/uwsgi --ini /usr/local/Quickstart-Secure-Django-Template/django_project/proj/uwsgi.ini'"
echo -e ""
echo -e "done."