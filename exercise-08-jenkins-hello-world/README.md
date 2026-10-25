# Exercise 8: Jenkins Hello World

Script repo: https://github.com/spurthi2509/devops-sample-code

## Part 1 (done)
Created hello-world.sh, committed it and pushed it to GitHub.

## Part 2
Jenkins freestyle job running `sh hello-world.sh` (to be added).

## Part 2: Jenkins job

A Freestyle project named `HelloWorld` was created in Jenkins (running in Docker, see Exercise 7).

- Source Code Management: Git, repository `https://github.com/spurthi2509/DevOps-Lab.git`, branch `*/main`.
- Build step (Execute shell): `sh exercise-08-jenkins-hello-world/hello-world.sh`
- Result: build #2 printed `Hello, Jenkins!` and finished with `Finished: SUCCESS`.
- Screenshot: `jenkins-console-output.png` (console output of build #2).

Build #1 cloned the repository and finished `SUCCESS`, but the Execute shell step had not been saved yet, so the script did not run. The step was added and build #2 was run.

### Changes from the instructor's instructions
- The separate `devops-sample-code` repository was not created. The job uses this submission repository instead.
- Branch is `*/main` (the manual's default is `*/master`), and the script path includes the folder `exercise-08-jenkins-hello-world/`.
