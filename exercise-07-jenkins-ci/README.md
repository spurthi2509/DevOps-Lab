# Exercise 7: Continuous Integration and Jenkins Installation

## Objective
Understand Continuous Integration (CI) and install Jenkins using Docker.

## Prerequisites
Windows laptop with Docker Desktop (WSL2).

## Commands used (Windows PowerShell)

    docker ps -a
    docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
    docker ps --filter name=jenkins
    docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

## What was done
1. Checked there was no existing `jenkins` container and nothing on port 8080.
2. Started Jenkins LTS in Docker, mapping ports 8080 (web UI) and 50000 (agents).
3. Read the one-time initial admin password from inside the container and used it to unlock Jenkins at `http://localhost:8080`.
4. Completed the setup wizard (suggested plugins, first admin user) and reached the Jenkins dashboard (Jenkins 2.580.1).

## Result
Jenkins is running and reachable on `http://localhost:8080`.

## Files
- `jenkins-status.txt` - `docker ps` output for the Jenkins container.
- `jenkins-image.txt` - `docker images` output for `jenkins/jenkins:lts`.
- `jenkins-dashboard.png` - screenshot of the Jenkins dashboard after setup.

## Changes from the instructor's instructions
- Added `-v jenkins_home:/var/jenkins_home` so Jenkins data persists across restarts, since the same instance is reused for Exercises 8 and 9.
- Ran `docker exec jenkins cat ...` directly instead of opening an interactive shell with `docker exec -it ... bash`.

## Security note
The initial admin password and the admin account password are not stored in this repository.
