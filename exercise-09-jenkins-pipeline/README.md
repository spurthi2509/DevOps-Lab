# Exercise 9: Jenkins Multi-Stage Pipeline (Python Flask App)

## Objective
Create a Jenkins Pipeline with Build, Test and Deploy stages for a small Python Flask application.

## Files
- `app.py` - Flask application that returns "Hello, Jenkins Multi-Stage Pipeline!".
- `test_app.py` - unit test for the home route.
- `requirements.txt` - Flask dependency (`flask==2.1.2`, from the instructions; see notes).
- `Jenkinsfile` - declarative pipeline with 5 stages: Build, Test, Deploy, Run Application, Test Application.

## Prerequisites
Jenkins running in Docker (Exercise 7) with the Pipeline plugin (installed with the suggested plugins). Python was installed inside the Jenkins container (Step 8 of the instructions), as root:

    docker exec -u root jenkins bash -c "apt-get update && apt-get install -y python3 python3-pip python3-venv python3-flask"

## Jenkins job configuration
- Job name: `Python-MultiStage-Pipeline` (type: Pipeline).
- Definition: Pipeline script from SCM, Git, repository `https://github.com/spurthi2509/DevOps-Lab.git`, branch `*/main`, no credentials.
- Script Path: `exercise-09-jenkins-pipeline/Jenkinsfile`

## Result
Build #1 ran all stages and finished with `Finished: SUCCESS` (commit `ed658b0`). The Test and Test Application stages each ran 1 test, `OK`. Inside the Jenkins container: Python 3.13.5 and Flask 3.1.1.

## Changes from the instructor's instructions
- The files live in this folder of my submission repository instead of a separate `devops-sample-code` repository, so each stage uses `dir('exercise-09-jenkins-pipeline')` and the Script Path points to this folder.
- The Build stage prints the Python and Flask versions instead of only echoing text. It does not run `pip install -r requirements.txt`: Flask came from the Debian package `python3-flask` (3.1.1) installed in the Jenkins container, so the pinned `flask==2.1.2` in `requirements.txt` was not used by the pipeline.
- The Build stage shows a harmless Flask deprecation warning about `flask.__version__`.
- Paths in the Jenkinsfile are relative to this folder instead of `${WORKSPACE}/...`.

## Notes and limitations
- The Test Application stage runs `test_app.py` again (Flask test client). It does not send an HTTP request to the application started in the Run Application stage.
- The packages installed in the Jenkins container live in the container itself. If the container is deleted and recreated, the install has to be repeated.

## Evidence files
- `jenkins-python-version.txt` - Python and Flask versions inside the Jenkins container.
- `jenkins-pipeline-console.png` - screenshot of the end of the Jenkins console output (build #1).
