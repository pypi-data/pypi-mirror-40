#!/opt/local/bin/bash
#
# Quick hack script to build a single gevent release in a virtual env. Takes one
# argument, the path to python to use.
# Has hardcoded paths, probably only works on my (JAM) machine.

set -e
export WORKON_HOME=$HOME/Projects/VirtualEnvs
export VIRTUALENVWRAPPER_LOG_DIR=~/.virtualenvs
source `which virtualenvwrapper.sh`

# Make sure there are no -march flags set
# https://github.com/gevent/gevent/issues/791
unset CFLAGS
unset CXXFLAGS
unset CPPFLAGS

BASE=`pwd`
BASE=`dirname $BASE`

cd /tmp/relstorage
virtualenv -p $1 `basename $1`
cd `basename $1`
echo "Made tmpenv"
echo `pwd`
source bin/activate
echo cloning $BASE
git clone $BASE
cd relstorage
pip install -U pip
pip install -U setuptools cffi
pip install -U wheel
python ./setup.py sdist bdist_wheel
cp dist/*whl /tmp/relstorage
