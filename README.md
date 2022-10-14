Steps for run Evase project:

1. install nodeJs, to enable npm command. link:  https://nodejs.org/en/download/
2. install python3
3. add npm, python and pip (a python package manageer) to system path(follow online link for each of them, similar but slightly diff).
4. using cmd navigate to api folder of the project
5. run command "pip install -r requirements.txt", This step is to install all the python packages needed.
6. back to the root folder, run command "npm install"
7. nevigate to client folder, run command "npm install" (same command for install nodeJs package, but at different level)
8. all package has been installed, next let's run it.
9. nevigate to client folder, run command "npm run start-api", this will start the backend flask server
10. stay in client folder, run "npm start", this will start react front end.
11. Project should be up and runnning.

Note: 
api folder is where flask and backend logic locate at
client folder is where the ReactJs files at
in api/api.py, the backend respond to file update is defined.
in client/src/EvaseApp.js is where the front end pages defined.

