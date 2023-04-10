[![CI Backend Tests](https://github.com/Bruce-liushaopeng/Evase/actions/workflows/ci_tests.yml/badge.svg?branch=main)](https://github.com/Bruce-liushaopeng/Evase/actions/workflows/ci_tests.yml)

# Evase Project

Welcome to the Evase project! Our aim is to detect attack vulnerabilities in your Python code.

## What's New?
- The first stable version of the project is available now!
- There have been many development improvements including the following
  - There was a previous poor design decision that the source code files would be re-read on the client-side every time a new node was selected
    - Now the nodes that represent vulnerabilities refer to another state variable containing the *previously read* code files
    - Code files are read once upon loading the project
  - The HTTP request functions have been separated into `util/Hooks.js`
    - This provides more separation of concerns
    - Await calls have been removed wherever used and replaced with `.then` calls on Promises
  - The user can see the `processing...` icon when the code is being loaded
  - Code deletion threads are actually now thread-safe!
    - They are now `daemon` threads
    - In case of faults, they are manually cancelled at program exit


## Installation and Setup Instructions

This project is to be containerized with docker, and deployment will be available with docker commands.
To download the project itself and run it without docker you can do:
- Clone the repository
- In the backend directory run `pip install -r requirements.txt`
- In the client directory run `npm install .` (use the force parameter if required)

## How to run Evase in local environment 

- Install all dependencies as described above
- In the backend directory run `python3 api.py` or `py api.py`
- In the frontend directory run `npm start`

## How to run Evase with docker

- Start docker desktop and wait for Docker and Kubernetes fully start
- go to .env file to define the ports that frontend and backend application will be listen to
- nevigate to home folder in the terminal
- run command `docker-compose build`, if not work, try `docker compose build`
- when build is finished, run command `docker-compose up` or `docker compose up`
- Go to browser and interact with the application
- To stop the running containers, run command "docker-compose down"

