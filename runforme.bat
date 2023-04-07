cd client
set install=%1

if install==1 npm install
if install==2 npm install --force

cd ../backend

START python -m flask run -h localhost -p 5050

cd ../client

START npm start
