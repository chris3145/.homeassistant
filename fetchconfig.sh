#!/bin/bash

cd "/home/homeassistant/.homeassistant/"

# This tries to do a standard git pull
# git pull origin master

# This scraps all local changes and then resets the branch to match.
# It basically says "Don't worry about changes I've made here, just copy the remote files."
git fetch
git reset --hard origin/master
