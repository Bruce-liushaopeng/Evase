FROM python:3.9-slim
WORKDIR /flask-docker
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /flask-docker
EXPOSE 5000
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]