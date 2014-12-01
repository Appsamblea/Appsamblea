#!/bin/sh
export GAE_DIR=/tmp/gae/google_appengine
export APP_DIR=.
echo "PR# $TRAVIS_PULL_REQUEST"
python $GAE_DIR/appcfg.py --oauth2_refresh_token=$GAE_OAUTH update $APP_DIR
