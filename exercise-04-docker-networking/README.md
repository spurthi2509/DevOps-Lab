# Exercise 4: Docker networking with multiple containers

Created a user-defined bridge network (my-bridge-net) and ran three containers on it: a Flask API, MySQL and Redis. Verified the Flask API from the host and checked name-based connectivity between containers.

## Files
- app.py, requirements.txt, Dockerfile: the Flask app
- network-*.txt: network create, list and inspect (before and after attaching containers)
- docker-ps.txt: the three running containers
- curl-about.txt, flask-about.png: Flask /about response
- ping-*.txt, flask-dns-check.txt: connectivity checks by container name

## Changes from the manual
- MySQL runs with MYSQL_ALLOW_EMPTY_PASSWORD=yes (it exits without a password setting, and no password is stored in this repo).
- app.py binds to 0.0.0.0 so the published port is reachable from the host.
- Python 3.11 and unpinned Flask, since Flask 2.0.1 breaks with current dependencies.
- ping is run from an alpine container on the same network, as the Flask image has no ping.

## Result
All three containers resolved each other by name on my-bridge-net, and /about returned the JSON response.
