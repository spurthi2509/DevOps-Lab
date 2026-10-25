# Exercise 5: Docker Security with AppArmor and Python

## Objective
Containerize a Flask app, define an AppArmor profile, apply it to the container with the Docker SDK for Python, and test restricted actions.

## Files
- `app.py` - Flask application (port 5000).
- `Dockerfile` - builds the `flask-apparmor` image from `python:3.8-slim`.
- `my-apparmor-profile` - AppArmor profile (`profile my-apparmor-profile flags=(attach_disconnected,mediate_deleted)`).
- `apply_apparmor.py` - builds the image, runs the container with `security_opt=["apparmor=my-apparmor-profile"]`, prints the applied option, stops the container.
- `test_restricted_actions.py` - tries `cat /etc/passwd` and `/bin/bash` inside the container.
- `docker-build-output.txt`, `apply-apparmor-output.txt`, `test-restricted-actions-output.txt` - real outputs from my machine.

## Environment
Windows laptop, Docker Desktop (WSL2), Python 3.11, Docker SDK 7.2.0.

## What was executed
1. `docker build -t flask-apparmor .` - succeeded.
2. `python apply_apparmor.py` - the container started and Docker reported `AppArmor profile applied: ['apparmor=my-apparmor-profile']`.
3. `python test_restricted_actions.py` - ran; results below.

## Actual results
| Action | Exit code | Manual expected |
|---|---|---|
| `cat /etc/passwd` | 0 (file contents printed) | 1 |
| `/bin/bash` | 0 | 126 |

## Limitation (important)
AppArmor is a Linux kernel feature and is not available in Docker Desktop for Windows (WSL2). The profile was **never loaded** with `apparmor_parser`, and **no enforcement was verified**. Docker accepted the `apparmor=my-apparmor-profile` option and recorded it, but the restricted actions were not blocked, so the outputs differ from the manual's expected ones. To see enforcement, run this on a Linux host with AppArmor:
`sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile`, then rerun the scripts.

## Changes from the manual
- Profile header changed to `profile my-apparmor-profile flags=(...) { ... }` so Docker can apply it by name.
- Added a `file,` rule and `abstractions/base`; narrowed the `/etc` deny to `/etc/passwd` and `/etc/shadow` so Python can still start.
- Added a `print` of the container id and a "Container stopped" message to the test script.
