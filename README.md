[![CI Backend Tests](https://github.com/Bruce-liushaopeng/Evase/actions/workflows/ci_tests.yml/badge.svg?branch=main)](https://github.com/Bruce-liushaopeng/Evase/actions/workflows/ci_tests.yml)

# Evase Project

Welcome to the Evase project! Our aim is to detect attack vulnerabilities in your Python code.

## Developer Instructions

- Test code should only be placed in the `api/user_files` directory
- Anthony's test code has been moved to a zip file under `examples/dool-test.zip`
  - You need to reload it into the `user_files` directory

## Installation and Setup Instructions

1. install nodeJs, to enable npm command. link:  https://nodejs.org/en/download/
2. install python3
3. add npm, python and pip (a python package manageer) to system path(follow online link for each of them, similar but slightly diff).
4. using cmd navigate to api folder of the project
5. run command "pip install -r requirements.txt", This step is to install all the python packages needed.
6. back to the root folder, run command "npm install"
7. nevigate to client folder, run command "npm install" (same command for install nodeJs package, but at different level)
8. all package has been installed, next let's run it.
9. nevigate to api folder, run command "npm run start-backend", this will start the backend flask server
10. stay in client folder, run "npm start", this will start react front end.
11. Project should be up and runnning.

